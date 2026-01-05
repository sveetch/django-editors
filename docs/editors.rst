.. _editors_intro:

Available editors
=================

TipTap
******

https://tiptap.dev/docs

TipTap is probably the most flexible and strong modern editor thanks to its base that
stand on ProseMirror. It is fully free except for some specific extensions like
collaboration or AI things.

https://tiptap.dev/docs/examples

We are providing a very minimal version in a bundle that just works but without any
feature you could expect from an editor. You may find a lot of guides and examples to
make your own improved bundle easily if you are working with React. Else you will need
some work achieve it yourself with different environment like VanillaJS, Vue, etc..


SunEditor
*********

https://github.com/JiHong88/suneditor/tree/develop

SunEditor is an editor which looks like "modernized CKEditor 4". It got the same look
and feel UI and technical behaviors but with an improved programmatic interface.

This is actually experimental since we are using the SunEditor V3 which is in beta
stage (in 'develop' branch).

Because it includes CSS stylesheets in its JavaScript component we need Webpack plugins
'css-loader' and 'MiniCssExtractPlugin' to build it.
