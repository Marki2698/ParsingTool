XML_FIELDS = {
    'FOLDER': 'folder',
    'NAME': 'name',
    'SRC': 'src',

}

XML_ATTRIBUTES = {
    'NAME': 'name',
    'MTIME': 'mtime',
    'FUNCTIONS_COVERED': 'fn_cov',
    'FUNCTIONS_TOTAL': 'fn_total',
    'CONDITIONS_COVERED': 'cd_cov',
    'CONDITIONS_TOTAL': 'cd_total',
    'DECISIONS_COVERED': 'd_cov',
    'DECISIONS_TOTAL': 'd_total'
}

CUSTOM_XML_FIELDS = {
    'FILES': 'files',
    'PROBES': 'probes',
    'FUNCTIONS': 'functions',
    'INFO': 'info',
    'FILE_PATH': 'path',
}

COLUMN_INDEXES = {
    'name': 1,
    'fn_cov': 2,
    'fn_uncov': 3,
    'fn_total': 4,
    'cd_cov_d_cov': 5,
    'cd_uncov_d_uncov': 6,
    'cd_total': 7,
    'd_total': 8,
    'path': 9
}

FIELDS_TO_PERCENTIZE = ['fn_cov', 'cd_cov_d_cov']

EXCLUDE_FIELDS = ['d_cov', 'cd_cov', ]

NAME_COLUMN = 'A:A'
FILENAME_HEADER_CELL = 'A1'
FUNCTION_NAME_COLUMN = 'B:B'
FILE_PATH_COLUMN = 'I:I'
HEADER_EXTENTION = '.h'
