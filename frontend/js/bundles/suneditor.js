/*
 * Editor class for SunEditor V3
 *
 * TODO: - What options ?
 *         - Tab key management option because on default Suneditor use four &nbsp;
 *           when tab key is pressed. This is not expected tab key behavior (on default
 *           indent on newline start or natural browser behavior to switch to another
 *           element;
 *       - How to enable plugins ?
 *       - Search if MiniCssExtractPlugin can produce CSS into '../css/' instead of
 *         the 'js/' directory.
 *       - Upgrade to final v3 release
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
    synchronizeInput(e) {
        this.editor.run("save");
    }

    /**
     * SunEditor does not need any preparation because it accords automatically to
     * any source element
     */
    prepareContainer() {}

    /**
    * Initialize, create and apply editor object.
    *
    * @return {Editor} - The created editor object.
    */
    provide() {
        // No need of preparing source because SunEditor will make all the job to
        // replace input
        this.container = this.source;

        const editor_options = {
            ...{
                events: {
                    onChange: (e) => {
                        if (this.is_sync) {
                            this.synchronizeInput(e);
                        }
                    }
                },
            },
            ...this.editor_options
        };

        this.editor = suneditor.create(
            this.container,
            editor_options
        );

        // Listen to form submit to synchronize editor content in input value
        if (this.attached_form) {
            this.attached_form.addEventListener("submit", (e) => {
                this.synchronizeInput(e);
            });
        }

        return this.editor;
    }
}


// Export to browser
window.DjangoSunEditor = DjangoSunEditor;
