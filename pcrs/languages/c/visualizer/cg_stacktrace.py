from languages.c.visualizer.cg_stacktrace_functions import *
import problems_c.models


class CVisualizer:
    """ Representation of C language in the visualizer platform
        * running tests
    """

    def __init__(self, user, temp_path):
        self.user = user
        self.temp_path = temp_path
        self.primitive_types = []

        # Printf hashkey to detect valid output
        self.key = hash_string((str(self.user) + str(get_current_date())).encode("utf-8"))

        # Get primitive types from database
        for primitive_type in problems_c.models.CPrimitiveTypes.objects.values_list():
            self.primitive_types.append({primitive_type[1]: primitive_type[2]})

    def build_stacktrace(self, user_script):

        user_script = remove_string_constant(user_script)
        extra_scape_sequence_list, user_script = add_break_line_after_token(user_script, [";", "{", "}"])

        # Process C source code
        stacktrace = []  # Stacktrace data structure
        line = ""  # Current source code line
        inside_function = False  # Program is examing the inside of a function
        analyze_declaration = False  # Program is examing a function/variable declaration
        line_count = 1
        declaration_type = ""  # Function/variable type
        other_brackets = 1
        function_brackets = []
        function_bracket_open_line = 0  # Function inner bracket open
        #function_bracket_close_line = 0  # Function inner bracket close

        for char in user_script:
            if char == '\n':

                # Search for variables and functions
                if not analyze_declaration:
                    declaration_type = search_dictionary(self.primitive_types, line)
                    if declaration_type != "":
                        analyze_declaration = True
                    elif not inside_function:
                        line = ""

                if analyze_declaration:
                    # Function declaration
                    if '(' in line and ')' in line and '{' in line and not inside_function:
                        dic = {'declaration': 'function', 'type': declaration_type,
                               'name': format_function_name(line, declaration_type),
                               'line_begin': line_count, 'scope': 'global', 'function_calls': [],
                               'return': [], 'variables': get_variables_details_func_signature(line, line_count)}
                        stacktrace.append(dic.copy())
                        inside_function = True
                        analyze_declaration = False
                        line = ""
                    # Prototype declaration
                    elif is_function_prototype(line):
                        line = ""
                        analyze_declaration = False
                    # Variable declaration
                    elif ';':
                        # Variable declaration inside function
                        if inside_function:
                            for local_var in get_variables_details(line, declaration_type):
                                malloc = False
                                if "malloc" in line:
                                    malloc = True
                                stacktrace[len(stacktrace)-1]['variables'].\
                                    append({line_count: [{local_var[0]: local_var[1]}, \
                                                         get_variable_location_inside_function(function_brackets),
                                                         {"malloc": malloc}]})
                            analyze_declaration = False
                        # Variable declaration outside function
                        elif not inside_function:
                            malloc = False
                            if "malloc" in line:
                                malloc = True
                            for global_var in get_variables_details(line, declaration_type):
                                dic = {'declaration': 'variable', 'type': global_var[0],
                                        'name': global_var[1], 'line': line_count,
                                        'scope': 'global', 'malloc': malloc}
                                stacktrace.append(dic.copy())
                            analyze_declaration = False
                            line = ""

                # Analyse attributes inside function, end of the function and other function calls
                if inside_function:
                    # Treat return statement as variable
                    if line.find("return") > -1:
                        malloc = False
                        if "malloc" in line:
                            malloc = True
                        stacktrace[len(stacktrace)-1]['return'].append(line_count)
                        stacktrace[len(stacktrace)-1]['variables'].\
                            append({line_count:
                                   {'return': {stacktrace[len(stacktrace)-1]['type']: get_return_variable(line)}, 'malloc': malloc
                                    }})
                    # Function calls
                    if is_function_call(line) and not analyze_declaration and\
                       search_dictionary(self.primitive_types, remove_bracket_value_range(line, "(", ")")) == "":
                        stacktrace[len(stacktrace)-1]['function_calls'].extend(get_function_call(line, line_count)[::-1])

                    # Language statement (if, else, for)
                    if is_language_statement(line):
                        line = ""
                        analyze_declaration = False

                    # Clean line and verify end of function
                    if line.find(";") > -1 or line.find("{") > -1 or line.find("}") > -1:
                        if line.find("{") > -1:
                            function_bracket_open_line = line_count
                            other_brackets += 1
                        if line.find("}") > -1:
                            function_bracket_close_line = line_count
                            function_brackets.append((function_bracket_open_line, function_bracket_close_line))
                            function_bracket_open_line = 0
                            other_brackets -= 1
                        # Function end
                        if other_brackets == 0:
                            stacktrace[len(stacktrace)-1]['line_end'] = line_count
                            del function_brackets[-1]  # Delete end of function bracket
                            stacktrace[len(stacktrace)-1]['brackets'] = function_brackets
                            inside_function = False
                            other_brackets = 1
                        analyze_declaration = False
                        line = ""

                # Do not consider extra line breaks added on source code pre processing
                if line_count in extra_scape_sequence_list:
                    extra_scape_sequence_list.remove(line_count)
                    line_count -= 1

                line_count += 1
            else:
                line += char

        return stacktrace

    def change_code_for_debbug(self, stacktrace, user_script):
        # Build printf statements for every single function line
        print_stack = []
        for res in stacktrace:
            if res['declaration'] == 'function':
                line = res['line_begin']
                print_list_func = get_global_printf_list(stacktrace, line, self.key, self.primitive_types)
                while line <= int(res['line_end']):
                    print_list_func = get_local_printf_list(stacktrace, line, res['name'], print_list_func, self.key,
                                                            self.primitive_types)
                    line += 1
                print_stack.append({(res['line_begin'], res['line_end']): print_list_func})


        # Include printf inside source code for compilation
        line_count = 1
        index = 0
        index_last_semicolon = 0
        script_size = len(user_script)
        print_inline_num = 0
        while index < script_size:
            line = remove_string_constant(user_script[index_last_semicolon: index+1])
            # Find end of statement to print object
            if line.find(";") > -1:
                # Find breaklines and count
                last_line = line_count
                line_count += len(list(find_all_occurrences(line, '\n')))
                for function in print_stack:
                    for function_line, print_details in function.items():
                        # Check if line is in print range
                        if line_count in range(function_line[0], function_line[1]+1):
                            append_line = ""
                            inline_functions_num = count_line_declarations(print_details, line_count)
                            if line_count != last_line:
                                print_inline_num = 0
                            # Find out if it is a inline declaration
                            line_start = line.rfind('{')+1 if line.rfind('{') > -1 else 0
                            if inline_functions_num > 1 and \
                               search_dictionary(self.primitive_types, line[line_start:].strip()) != "":
                                print_inline_num += 1
                            print_inline_num_tmp = print_inline_num
                            for print_statement in print_details:
                                for line_start, print_string in print_statement.items():
                                    # Return statements
                                    if str(line_start) == 'return':
                                        if str(line_count) in print_string:
                                            print_string_tmp = print_string[str(line_count)].replace("<line>",
                                                                                                     str(line_count))
                                            #append_line += print_string_tmp
                                    # Other statements
                                    elif line_count >= int(line_start):
                                        if inline_functions_num > 1 and print_inline_num_tmp == 0:
                                            break
                                        print_string_tmp = print_string.replace("<line>", str(line_count))
                                        append_line += print_string_tmp
                                        if line_count == int(line_start):
                                            print_inline_num_tmp -= 1
                            user_script = insert_substring_in_string(user_script, append_line, index+1)
                            script_size += len(append_line)
                            index += len(append_line)
                    index_last_semicolon = index+1  # Jump to next character after the semicolom
            index += 1

        # include the standard input/output library
        user_script = insert_substring_in_string(user_script, "#include <stdio.h>\n", 0)

        return user_script

    def get_visualizer_enconding(self, code_output):

        import re
        r = re.compile("\("+self.key+"\)"+'(.*?)'+"\("+self.key+"\)")
        visualizer_trace = []
        line_num = ""

        lines_info = code_output['test_val'].split('\n')
        lines_info = [line for line in lines_info if line != '']

        j = -1
        for i in range(len(lines_info)):

            line = lines_info[i]
            ret = r.search(line)
            if ret:
                values = ret.group(1)
                values_list = values.split(";")
                if '*' in values_list[2]:
                    values_list[2] = values_list[2][1:]
                    values_list[1] += '*'

                if line_num == values_list[0]:
                    visualizer_trace[j].append(values_list)
                else:
                    line_num = values_list[0]
                    j += 1
                    visualizer_trace.append([values_list])

        return visualizer_trace

