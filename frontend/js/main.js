/*
 * Main frontend Javascript entrypoint.
*/

//
// Make Bootstrap components usable from templates (like "bootstrap.Modal(..)")
//
window.bootstrap = require("bootstrap/dist/js/bootstrap.bundle.js");

//
// Make Bootstrap components usable inside modules (directly through component name)
// You may disable unused components to lighten builded JS file
//
import {
    Alert,
    Button,
    // Carousel,
    Collapse,
    Dropdown,
    Modal,
    // Popover,
    // ScrollSpy,
    Tab,
    // Toast,
    // Tooltip,
} from "bootstrap/dist/js/bootstrap.bundle.js";

//
// NOTE: Sample how to instanciate a Bootstrap component object.
//
// var myModal = new Modal(document.getElementById("exampleModalDefault"));
// myModal.show();
