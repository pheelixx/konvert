# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from document import Document
from image import Image


class Settings():
    convert_routes = {
        'pdf': {
            'docx': Document
        },
        'ppt': {
            'odp': Document,
            'pdf': Document
        },
        'csv': {
            'xls': Document
        },
        'xls': {
            'ods': Document,
            'pdf': Document
        },
        'xlsx': {
            'ods': Document,
            'pdf': Document
        },
        'ods': {
            'xls': Document,
            'xlsx': Document
        },
        'doc': {
            'odt': Document,
            'pdf': Document
        },
        'docx': {
            'doc': Document,
            'odt': Document
        },
        'odt': {
            'doc': Document,
            'docx': Document
        },
        'jpg': {
            'png': Document, #Image,
            'pdf': Document
        },
        'jpeg': {
            'png': Document, #Image,
            'pdf': Document
        },
        'png': {
            'jpg': Document, #Image,
        },
        'bmp': {
            'png': Document, #Image,
            'jpeg': Document, #Image,
        }
    }

    types = {
        '.pdf':  'application/pdf',
        '.ppt':  'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.odp':  'application/vnd.oasis.opendocument.presentation',
        '.csv':  'text/csv',
        '.xls':  'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ods':  'application/vnd.oasis.opendocument.spreadsheet',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc':  'application/msword',
        '.odt':  'application/vnd.oasis.opendocument.text',
        '.jpg':  'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png':  'image/png',
        '.bmp':  'image/bmp',
    }

    extensions = {
        'application/pdf': 'pdf',
        'application/vnd.ms-powerpoint': 'ppt',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
        'application/vnd.oasis.opendocument.presentation': 'odp',
        'text/csv': 'csv',
        'application/vnd.ms-excel': 'xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
        'application/vnd.oasis.opendocument.spreadsheet': 'ods',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/msword': 'doc',
        'application/vnd.oasis.opendocument.text': 'odt',
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/bmp': 'bmp',
    }
