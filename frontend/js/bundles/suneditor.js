/*
 * Editor class for SunEditor V3
 *
 * TODO: - How to save editor into input for submitting form ? Dig into its code.
 *       - What options ?
 *       - How to enable plugins ?
 *       - Search if MiniCssExtractPlugin can produce CSS into '../css/' instead of
 *         the 'js/' directory.
 */

import "suneditor/css"; // Editor UI
import "suneditor/css/contents"; // For displaying HTML
import suneditor from "suneditor";

import { DjangoBaseEditor } from "../modules/base_editor";

/**
 * Very minimal implementation of SunEditor
 */
class DjangoSunEditor extends DjangoBaseEditor {
    /**
     * Save editor content into source value
     */
    synchronizeInput() {}

    /**
     * SunEditor does not need any preparation since it flex itself according to
     * source element
     */
    prepare() {}

    /**
    * Initialize, create and apply editor object.
    *
    * @return {Editor} - The created editor object.
    */
    provide() {
        // No need of preparing source
        this.container = this.source;

        this.editor = suneditor.create(this.container, {
            // plugins: ["font", "image", "video"],
        });

        return this.editor;
    }
}


// Export to browser
window.DjangoSunEditor = DjangoSunEditor;
