function create_history_code_mirror(language,version,location){hcm=history_code_mirror(language,version,$('#'+location),$('#'+location).text(),true);if(!(location in cmh_list)){cmh_list[location]=hcm;}}
function history_code_mirror(language,version,location,value,lock){var mode;if(language=='python'){mode={name:language,version:version,singleLineStringErrors:false}}
else if(language=='sql'){mode='text/x-plsql';}
else if(language=='ra'){mode='text/ra';}
else if(language=='c'){mode='text/x-csrc';}
historyCodeMirror=CodeMirror(function(elt){$(location).replaceWith(elt);},{mode:mode,theme:user_theme,value:value,lineNumbers:'True',indentUnit:4,readOnly:lock,lineWrapping:'True',flattenSpans:'False'});return historyCodeMirror;}
var cmh_list={};var language;var language_version;var id_starter_code_field='id_starter_code';var id_solution_field='id_solution';var id_preview_code_field='id_preview_code';var blocked_list=[],hidden_list=[],student_code_list=[];var last_starter_code_cursor_position=null;function add_student_code_tag(){var line_count=cmh_list[id_starter_code_field].lineCount();var i;var line;var source_code="";var student_code_tag_open=false;var some_tag_open=0;var just_closed=false;var student_code_tag_count=0;for(i=0;i<line_count;i++){line=cmh_list[id_starter_code_field].getLine(i);if(line.indexOf("[blocked]")>-1||line.indexOf("[hidden]")>-1||line.indexOf("[student_code]")>-1){if(line.indexOf("[student_code]")>-1){student_code_tag_count+=1;}
some_tag_open+=1;}
if(line.indexOf("[/blocked]")>-1||line.indexOf("[/hidden]")>-1||line.indexOf("[/student_code]")>-1){some_tag_open-=1;just_closed=true;}
if(some_tag_open==0&&just_closed==false&&student_code_tag_open==false){source_code+="[student_code]\r\n"+line+'\n';student_code_tag_count+=1;student_code_tag_open=true;}else if(some_tag_open>0&&student_code_tag_open==true){source_code+="[/student_code]\r\n"+line+'\n';student_code_tag_open=false;}else{source_code+=line+'\n';}
just_closed=false;}
if(student_code_tag_count==0){source_code+="[student_code]\r\n\n";student_code_tag_open=true;}else{source_code=source_code.substring(0,source_code.length-1);}
if(student_code_tag_open==true){source_code+="\n[/student_code]";}
return source_code;}
function submitHidden(){var source_code=add_student_code_tag();document.getElementById("id_starter_code_tmp").value+=source_code;document.getElementById("id_solution_tmp").value+=cmh_list[id_solution_field].getValue();}
function detectTags(){var line_count=cmh_list[id_starter_code_field].lineCount();var i;var line;var blocked_open=0;var hidden_open=0;var student_code_open=0;blocked_list=[];hidden_list=[];student_code_list=[];for(i=0;i<line_count;i++){line=cmh_list[id_starter_code_field].getLine(i);if((line.split("[blocked]").length-1)>0){blocked_list.push({"start":i+1,"end":0});blocked_open+=1;continue;}
if((line.split("[/blocked]").length-1)>0){blocked_list[blocked_open-1].end=i+1;continue;}
if((line.split("[hidden]").length-1)>0){hidden_list.push({"start":i+1,"end":0});hidden_open+=1;continue;}
if((line.split("[/hidden]").length-1)>0){hidden_list[hidden_open-1].end=i+1;continue;}
if((line.split("[student_code]").length-1)>0){student_code_list.push({"start":i+1,"end":0});student_code_open+=1;continue;}
if((line.split("[/student_code]").length-1)>0){student_code_list[student_code_open-1].end=i+1;}}}
function createTag(tag_start,tag_end){detectTags();var i;var selection_begin=cmh_list[id_starter_code_field].getCursor(true).line+1;for(i=0;i<blocked_list.length;i++){if(selection_begin>=blocked_list[i].start&&selection_begin<=blocked_list[i].end)
if(tag_start=='[blocked]'||tag_start=='[student_code]'){document.getElementById("tag-error-message").innerHTML="<p>Check your code selection!</p><p>Cannot include blocked or student_code tags inside a blocked section, or along the same line.</p>";$('#tagModal').modal('show');return}}
for(i=0;i<hidden_list.length;i++){if(selection_begin>=hidden_list[i].start&&selection_begin<=hidden_list[i].end)
if(tag_start=='[blocked]'||tag_start=='[student_code]'||tag_start=='[hidden]'){document.getElementById("tag-error-message").innerHTML="<p>Check your code selection!</p><p>Cannot include any other tag inside a hidden section, or along the same line.</p>";$('#tagModal').modal('show');return}}
for(i=0;i<student_code_list.length;i++){if(selection_begin>=student_code_list[i].start&&selection_begin<=student_code_list[i].end)
if(tag_start=='[blocked]'||tag_start=='[student_code]'||tag_start=='[hidden]'){document.getElementById("tag-error-message").innerHTML="<p>Check your code selection!</p><p>Cannot include any other tag inside a student_code section, or along the same line.</p>";$('#tagModal').modal('show');return}}
var selected_area=cmh_list[id_starter_code_field].getSelection();cmh_list[id_starter_code_field].replaceSelection(tag_start+'\n'+selected_area+'\n'+tag_end);}
function updateCodeHighLight(){var code_highlight=0;var line_begin=cmh_list[id_starter_code_field].firstLine();var line_end=cmh_list[id_starter_code_field].lastLine();for(var i=line_begin;i<=line_end;i++){var line=cmh_list[id_starter_code_field].getLine(i);if(line.indexOf("[hidden]")>-1||line.indexOf("[blocked]")>-1||line.indexOf("[student_code]")>-1)
code_highlight+=1;if(code_highlight>0)
cmh_list[id_starter_code_field].addLineClass(i,'','CodeMirror-activeline-background');else
cmh_list[id_starter_code_field].removeLineClass(i);if(line.indexOf("[/hidden]")>-1||line.indexOf("[/blocked]")>-1||line.indexOf("[/student_code]")>-1)
code_highlight-=1;}}
function previewCode(){cmh_list[id_starter_code_field].setValue(add_student_code_tag());detectTags();var remove_line=false;var student_code_start=false;var student_code_end=false;var source_code="";var line_begin=cmh_list[id_starter_code_field].firstLine();var line_end=cmh_list[id_starter_code_field].lastLine();var line;var j;for(var i=line_begin;i<=line_end;i++){line=cmh_list[id_starter_code_field].getLine(i);for(j=0;j<blocked_list.length;j++){if(blocked_list[j].start==i+1||blocked_list[j].end==i+1){remove_line=true;}}
for(j=0;j<hidden_list.length;j++){if(hidden_list[j].start<=i+1&&hidden_list[j].end>=i+1){remove_line=true;}}
for(j=0;j<student_code_list.length;j++){if(student_code_list[j].start==i+1){student_code_start=true;}else if(student_code_list[j].end==i+1){student_code_end=true;}}
if(remove_line==false&&line!=" "){if(student_code_start==true){source_code+='//Implementation start';student_code_start=false;}
else if(student_code_end==true){source_code+='//Implementation end';student_code_end=false;}else{source_code+=cmh_list[id_starter_code_field].getLine(i);}
if(i<line_end){source_code+='\n';}}
remove_line=false;}
if(source_code[source_code.length-1]=='\n')
source_code=source_code.substring(0,source_code.length-1);if(cmh_list[id_preview_code_field]!=null){cmh_list[id_preview_code_field].setValue(source_code);}else{cmh_list[id_preview_code_field]=history_code_mirror(language,language_version,$('#'+id_preview_code_field),source_code,true);}
$('#previewModal').on('shown.bs.modal',function(){cmh_list[id_preview_code_field].refresh();});$('#previewModal').modal('show');}
function blockInput(editor_id,change){var line=cmh_list[editor_id].getLine(cmh_list[editor_id].getCursor().line);var line_size=line.length;if((line.lastIndexOf("[hidden]")>-1&&line_size>="[hidden]".length)||(line.lastIndexOf("[blocked]")>-1&&line_size>="[blocked]".length)||(line.lastIndexOf("[student_code]")>-1&&line_size>="[student_code]".length)||(line.lastIndexOf("[/hidden]")>-1&&line_size>="[/hidden]".length)||(line.lastIndexOf("[/blocked]")>-1&&line_size>="[/blocked]".length)||(line.lastIndexOf("[/student_code]")>-1&&line_size>="[/student_code]".length)){change.cancel();}
last_starter_code_cursor_position=cmh_list[editor_id].getCursor();}
$(function(){language='c';language_version='text/x-csrc';document.getElementById("submit-id-submit").setAttribute("onclick","return submitHidden();");var element=document.getElementsByTagName('form')[0];element.innerHTML=element.innerHTML+'<input type="hidden" id="id_starter_code_tmp" name="starter_code" value=""></input>';element.innerHTML=element.innerHTML+'<input type="hidden" id="id_solution_tmp" name="solution" value=""></input>';$('#div_'+id_starter_code_field).after('<a class="btn btn-danger" role="button" onclick="createTag('+"'[hidden]','[/hidden]'"+')"><span class="glyphicon glyphicon-eye-close"></span>  Hidden</a>');$('#div_'+id_starter_code_field).after('<a class="btn btn-danger" role="button" onclick="createTag('+"'[blocked]','[/blocked]'"+')"><span class="glyphicon glyphicon-ban-circle"></span>  Blocked</a>&nbsp;&nbsp;&nbsp;');$('#div_'+id_starter_code_field).after('<a class="btn btn-success" role="button" onclick="createTag('+"'[student_code]','[/student_code]'"+')"><span class="glyphicon glyphicon-pencil"></span>  Student Code</a>&nbsp;&nbsp;&nbsp;');$('#div_'+id_starter_code_field).after('<a class="btn btn-primary" role="button" onclick="previewCode()"><span class="glyphicon glyphicon-eye-open"></span>  Preview Exercise</a>&nbsp;&nbsp;&nbsp;');cmh_list[id_starter_code_field]=history_code_mirror(language,language_version,$('#'+id_starter_code_field),$('#'+id_starter_code_field).text(),false);cmh_list[id_solution_field]=history_code_mirror(language,language_version,$('#'+id_solution_field),$('#'+id_solution_field).text(),false);last_starter_code_cursor_position=cmh_list[id_starter_code_field].getCursor();cmh_list[id_starter_code_field].on("change",updateCodeHighLight);cmh_list[id_starter_code_field].on("beforeChange",function(instance,change){blockInput(id_starter_code_field,change);});updateCodeHighLight();$(window).bind("load",function(){$('.CodeMirror').each(function(i,el){el.CodeMirror.refresh();});});});