/**
 *
 * @param id
 * @constructor
 */
function NavGraph (id) {
    this.name = id;
}


/**
 * Updates the nav-graphs nodes to reflect active nodes in the main graph.
 * @param node The selected node in the graph. This node is updated in the
 * nav-graph.
 */
NavGraph.prototype.updateNode = function (node) {
    "use strict";
    var newId = '#' + node.attr('id') + '-map-node';
    $(newId).attr('data-active', 'display-selected');
};


/**
 * Removes all arrow heads from this NavGraph.
 */
NavGraph.prototype.removeArrowHeads = function () {
    "use strict";
    $('#nav-graph').find('polygon').remove();
};


/**
 * Sets the IDs of the elements associated with the NavGraph.
 */
NavGraph.prototype.setupIDs = function () {
    "use strict";
    $('#nav-graph').find('.node').each(function () {
        $(this).attr('id', $(this).attr('id') + '-map-node');
    });
};


/**
 *
 */
NavGraph.prototype.removeText = function () {
    "use strict";
    $('#nav-graph').find('text').remove();
};