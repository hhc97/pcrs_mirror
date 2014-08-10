/**
 * Sets the mouse callbacks for the nodes.
 */
function setMouseCallbacks() {
    "use strict";
    var nodeObjects = $('#graph').find('.node');
    nodeObjects.click(function (event) {
        turnNode(event);
    })
        .mouseenter(function (event) {
            updateParentCount($(this).children('.counter-text'), true);
            hoverFocus(event);
        })
        .mouseleave(function (event) {
            updateParentCount($(this).children('.counter-text'), false);
            hoverUnfocus(event);
        });
}