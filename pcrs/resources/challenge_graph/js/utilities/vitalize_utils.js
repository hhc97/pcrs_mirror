/**
 * Returns whether px and py intersects with a rectangle starting at rx and ry, with corresponding widths and heights
 * to the parameters.
 * @param px The x position of the evaluated point.
 * @param py The y position of the evaluated point.
 * @param rx The x start point of the evaluated rectangle.
 * @param ry The y start point of the evaluated rectangle.
 * @param width The width of the evaluated rectangle.
 * @param height The height of the evaluated rectangle.
 * @param offset The offset of the intersection.
 * @returns {boolean} Whether the evaluated point intersects with the evaluated rectangle with the calculated offset.
 */
function intersects(px, py, rx, ry, width, height, offset) {
    "use strict";
    var dx = px - rx;
    var dy = py - ry;
    return dx >= -1 * offset && dx <= width + offset && dy >= -1 * offset && dy <= height + offset;
}


/**
 * The hover event for a Node.
 * @param event
 */
function hoverFocus(event) {
    "use strict";
    var id = event.target.parentNode.id;
    window[id].focus();
}


/**
 * The unhover event for a Node.
 * @param event
 */
function hoverUnfocus(event) {
    "use strict";
    var id = event.target.parentNode.id;
    window[id].unfocus();
}


/**
 * Gets the JSON object produced for the current user.
 * @returns {*} The JSON object of the current user's challenge data.
 */
function getJSON() {
    "use strict";
    var json = null;
    $.ajax({
        url: 'prereq_graph/for_user',
        dataType: 'text',
        async: false,
        success: function (data) {
            json = data;
        }
    });
    return $.parseJSON(json);
}


/**
 * Creates an svg rect and appends it to #graph0.
 * @param posX The x position of the rect.
 * @param posY The y position of the rect.
 * @param width The width of the rect.
 * @param height The height of the rect.
 * @param color The fill and stroke color of the rect.
 */
function createRect(posX, posY, width, height, color) {
    "use strict";
    $('#graph0').append($(document.createElementNS(
        'http://www.w3.org/2000/svg', 'rect')).attr({
        x: posX,
        y: posY,
        rx: 20,
        ry: 20,
        fill: color,
        stroke: color,
        width: width,
        height: height
    }));
}
