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
 * Sets the main svg graph id.
 * Note: This is necessary in the JavaScript. It cannot be put into Beautiful
 * Soup because the generated svg is duplicated in the HTML.
 */
function setMainGraphID() {
    "use strict";
    $('svg:first').attr('id', 'graph');
}