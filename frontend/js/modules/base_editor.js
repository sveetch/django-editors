/*
 *
 * Django editor basic abstract
 *
 * TODO: 'form' or 'sync' won't do anything if the source element is not an input. So
 * we may need an additional option like 'target_input' that could be used to carry
 * editor content value to be submitted.
 */


/**
 * Editor abstract class
 *
 * Abstraction to inherit to implement the shared way to initialize an editor. This is
 * formerly called the "editor wrapper".
 *
 * Basically the input source is not automatically updated with editor content, either
 * use argument 'form' or 'sync' to enable the prefered behavior, avoid to use them
 * both, commonly the 'sync' argument is recommended choice.
 *
 *
 * @param {HTMLElement} source - Source element for the editor, it must have an 'id'
 *                      attribute value.
 * @param {string} initial - Initial editor value to force over the possible source
 *                 content value. This is not recommended when source is a form control
 *                 because whatever you input, after a submit the initial value will
 *                 overwrite it in the form control.
 * @param {object} editor_options - Options to give to editor during initialization.
 *                 Passing options to editor is left to concrete 'DjangoBaseEditor'
 *                 implementation in 'provide()' method. This is an empty object on
 *                 default.
 * @param {object} wrapper_options - Options for the wrapper itself.
 * @param {string} classNames - CSS class names to append onto container element.
 *
 * Wrapper options:
 *
 * @param {HTMLElement} form - Form element where the editor will edit an input. This
 *                      is currently only used to listen to 'submit' event from form.
 *                      WARNING: If you mount editor on a required input, the browser
 *                      will block the submit event because of "Constraint Validation
 *                      API" and so either you remove the required constraint from input
 *                      or you apply the 'novalidate' attribute on the form.
 * @param {boolean} sync - Enable synchronizing editor content into input on editor
 *                  content changes (as when typing something).
 */
export class DjangoBaseEditor {
    constructor(args) {
        this.validate(args);

        this.editor = null;
        this.source = args.source;
        this.editor_options = args.editor_options || {};
        this.wrapper_options = args.wrapper_options || {};
        this.initial = args.initial || "";
        this.classNames = args.classNames || "";
        this.container = null;

        /*
        console.log("🏗️constructor");
        console.log("this.source:", this.source.id);
        console.log("this.editor_options:", this.editor_options);
        console.log("this.wrapper_options:", this.wrapper_options);
        console.log("this.initial:", this.initial);
        console.log("this.classNames:", this.classNames);
        console.log("this.is_sync:", this.is_sync);
        console.log("this.attached_form:", this.attached_form);
        console.log("this.wrapper_options:", this.wrapper_options);
        */

    }

    /**
     * Getter for wrapper option 'sync'
     */
    get is_sync() {
        return this.wrapper_options["sync"] === true ? true : false;
    }

    /**
     * Setter for wrapper option 'sync'
     */
    set is_sync(value) {
        this.wrapper_options["sync"] = value;
    }

    /**
     * Getter for wrapper option 'form'
     *
     * If 'form' value from wrapper option is a string, we assume it is a selector to
     * resolve from current document. If it is not a string it is return unchanged
     * because we assume it is an HTMLElement.
     */
    get attached_form() {
        if(
            this.wrapper_options["form"]
            && typeof this.wrapper_options["form"] === 'string'
        ) {
            return document.querySelector(this.wrapper_options["form"]);
        }

        return this.wrapper_options["form"];
    }

    /**
     * Setter for wrapper option 'form'
     */
    set attached_form(value) {
        this.wrapper_options["form"] = value;
    }

    /**
     * Determine if given source element is a form control or not.
     *
     * @param {HTMLElement} source - Source element to check.
     *
     * @return {boolean} - True if source is a form control (input or textarea) else
     *                     False.
     */
    isFormControl(source) {
        if (source.tagName === "INPUT" || source.tagName === "TEXTAREA") {
            return true;
        }

        return false;
    }

    /**
     * Validate editor class configuration
     *
     * @return {boolean} -
     */
    validate(args) {
        if(!args.source) {
            throw new Error("The argument 'source' can not be empty");
        }
    }

    /**
     * Prepare container element before attaching editor
     *
     * Some editor can only work on non form control element (like a textarea) so we
     * need to create a virtual div where to push the editor. In this case the source
     * should be synchronized from editor content.
     *
     * @return {HTMLElement} - The element where to concretely attach the editor. Basically
     *                         it would be the one given in 'source' parameter except if
     *                         it is not a proper element to include the editor (like a
     *                         textarea or an input), in this case the source is hidden and
     *                         a new 'div' is created and returned so the editor will be
     *                         attached on it instead.
     *
     *                         When source element is replaced by a div, source will have
     *                         an attribute 'data-replacement' and div will have an
     *                         attribute 'data-source' both filled with an element
     *                         identifier referencing their brother.
     */
    prepareContainer() {
        if(!this.source) {
            throw new Error("The argument 'source' can not be empty");
        }

        // Only replace a source element that is not a valid container for the editor
        // elements
        if (this.isFormControl(this.source) === true) {
            // Hide real target
            this.source.style.display = "none";

            // Create a div element with a right ID
            const replacement = document.createElement("div");
            replacement.id = this.source.id + "_editor";

            // add data for the brother selector
            replacement.dataset.source = "#" + this.source.id;
            this.source.dataset.replacement = "#" + replacement.id;

            // add CSS classes
            if (this.classNames) {
                replacement.className = this.classNames;
            }

            // if input has a value copy it to this.initial if args.initial
            // was not empty
            if (!this.initial && this.source.value) {
                this.initial = this.source.value;
            // Else if there is initial value from args set on source value
            } else if (this.initial) {
                this.source.value = this.initial;
            }

            // Append created div to DOM just after/before the real target
            this.source.parentNode.insertBefore(replacement, this.source.nextSibling);

            // Returns the created div element object
            return replacement;
        }

        // Append CSS classnames
        if (this.classNames) {
            this.source.className = this.classNames;
        }

        return this.source;
    }

    /**
     * Save editor content into source value
     *
     * Commonly used to set input value according to editor content when submitting
     * form. This does nothing if source is not a form control.
     *
     * @param {Any} e - parameter argument that is commonly an Event object. However it
     *              is not used in common editor implementation that prefer to directly
     *              use the editor instance from 'this.editor'. Editor wrappers are
     *              responsible to bind event on this method so finally it could be
     *              any type.
     */
    synchronizeInput(e) {}

    /**
     * Initialize, create and apply editor object.
     *
     * This is where to implement editor initialization.
     *
     * @return {Editor} - The created editor object.
     */
    provide() {
        this.container = this.prepareContainer();

        return this.editor;
    }
}
