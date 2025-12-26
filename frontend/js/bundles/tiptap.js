import { Editor } from '@tiptap/core'
import StarterKit from '@tiptap/starter-kit'

new Editor({
    element: document.querySelector('.editor-sample__integration'),
    extensions: [StarterKit],
    content: '',
});
