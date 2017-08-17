__author__ = 'alex'


CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'Standard',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['-', 'Iframe', ],
            ['RemoveFormat', 'Source'],
            ['Image', 'Styles'],
            ['FontSize', 'Format', 'Font', 'TextColor', 'BGColor'],
            ['Maximize'],
            ['Undo', 'Redo'],
        ],
        'height': 400,
        'width': 800,
        'skin': 'minimalist',
    },
}


CKEDITOR_UPLOAD_PATH = "uploads/"

# Full CKEDITOR ITEMS
# config.toolbar = 'Full';
#
# config.toolbar_Full =
# [
# 	{ name: 'document', items : [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ] },
# 	{ name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
# 	{ name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
# 	{ name: 'forms', items : [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
#         'HiddenField' ] },
# 	'/',
# 	{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
# 	{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv',
# 	'-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
# 	{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
# 	{ name: 'insert', items : [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ] },
# 	'/',
# 	{ name: 'styles', items : [ 'Styles','Format','Font','FontSize' ] },
# 	{ name: 'colors', items : [ 'TextColor','BGColor' ] },
# 	{ name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','About' ] }
# ];
#
# config.toolbar_Basic =
# [
# 	['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink','-','About']
# ];