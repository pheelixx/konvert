# coding: utf-8
__author__ = 'Stanislav Varnavsky'

import uno
# from tools import Tools
from os.path import abspath


class Document:
    document = None
    properties = []
    # arguments:
    #   DocumentBaseURL
    #   UCBContent
    #   Stream
    #   Title
    #   URL
    #   FilterName
    #   InteractionHandler
    #   UpdateDocMode
    #   MacroExecutionMode
    #   DocumentService
    #   DocumentBorder
    #   WinExtent
    arguments = {}
    statistics = {}
    path = ''
    filter = ''
    service = ''
    border = ''
    extent = ''
    relations = {
        'doc': ['pdf', 'docx', 'odt'],
        'xls': ['xlsx'],
        'ppt': ['pptx']
    }
    # imp = {
    #     'writer_pdf_Export':    'pdf',
    #     'writer8_template':     'odt',
    #     'MS Word 97':           'doc',
    #     'MS Word 97 Vorlage':   'doc'
    # }
    export_options = {
        'pdf': {
            'FilterName': 'writer_pdf_Export',
            # @url https://wiki.openoffice.org/wiki/API/Tutorials/PDF_export
            'FilterData': {
                'PageRange': '1-20',
                'Quality': 5,
                'MaxImageResolution': 75,
                'EmbedStandardFonts': False
            }
        },
        'odt': {
            'FilterName': 'writer8',
            'FilterData': {
                # 'PageRange': '1-20',
                # 'Quality': 5,
                # 'MaxImageResolution': 75,
                # 'EmbedStandardFonts': False
            }
        }
    }
    connection_string = "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
    resolver_instance = "com.sun.star.bridge.UnoUrlResolver"

    def __init__(self, path):
        self.path = path
        context = uno.getComponentContext()
        resolver = context.ServiceManager.createInstanceWithContext(Document.resolver_instance, context)
        context = resolver.resolve(Document.connection_string)
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        self.document = desktop.loadComponentFromURL(uno.systemPathToFileUrl(abspath(path)), "_blank", 0, tuple([]))
        if hasattr(self.document, 'getArgs'):
            documentProperties = self.document.getDocumentProperties()
            if len(documentProperties) is not 0:
                statistics = documentProperties.DocumentStatistics
                for current in statistics:
                    self.statistics[current.Name] = current.Value
            for argument in self.document.getArgs():
                self.arguments[argument.Name] = argument.Value
            # https://wiki.openoffice.org/wiki/Framework/Article/Filter/FilterList_OOo_3_0
            self.filter = self.arguments['FilterName']          # "MS Word 97 Vorlage"
            self.service = self.arguments['DocumentService']    # "com.sun.star.text.TextDocument"
            self.border = self.arguments['DocumentBorder']      # "(0L, 0L, 12534L, 7227L)"
            self.extent = self.arguments['WinExtent']           # "(25L, 25L, 16L, 16L)"
            # /usr/local/www/upload/2/11c3a3f9ec9f6e80098ec8ccd3bbdd50

    def __del__(self):
        self.close()

    def get(self, path):
        return self.document

    def save(self, path):
        from tools import Tools
        if not hasattr(self.document, 'getArgs'):
            return False
        # import_extension = self.imp[self.filter]
        if len(self.properties) == 0:
            export_extension = Tools.get_extension(path)
            properties = self.export_options[export_extension]
            self.set_properties(properties)
        self.document.storeToURL(uno.systemPathToFileUrl(abspath(path)), tuple(self.properties))
        return True

    def set_property(self, name, value):
        property = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
        property.Name = name
        property.Value = value
        self.properties.append(property)
        del property

    def set_properties(self, properties):
        for name, value in properties.iteritems():
            if type(value).__name__ == 'dict':
                value = self.__build_properties_recursively(value)
            property = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            property.Name = name
            property.Value = value
            self.properties.append(property)
            del property

    def __build_properties_recursively(self, properties):
        data = []
        for name, value in properties.iteritems():
            if type(value).__name__ == 'dict':
                value = self.__build_properties_recursively(value)
            property = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
            property.Name = name
            property.Value = value
            data.append(property)
        return uno.Any("[]com.sun.star.beans.PropertyValue", tuple(data))

    def close(self):
        if hasattr(self.document, 'getArgs'):
            self.document.close(True)

    @staticmethod
    def get_settings(extension):
        options = Document.export_options[extension]
        return options['FilterData']

    def get_statistics(self):
        statistics = {}
        labels = {
            'CharacterCount': 'Count of Characters',
            'ImageCount': 'Count of Images',
            'NonWhitespaceCharacterCount': 'Count of Non-Whitespace Characters',
            'ObjectCount': 'Count of Objects',
            'PageCount': 'Count of Pages',
            'ParagraphCount': 'Count of Paragraphs',
            'TableCount': 'Count of Tables',
            'WordCount': 'Count of Words',
        }
        for key, value in self.statistics.iteritems():
            label = key
            if label in labels:
                label = labels[key]
            statistics[label] = value
        return statistics

    def get_export_options(self, extension=None):
        pageCount = 1
        if 'PageCount' in self.statistics:
            pageCount = self.statistics['PageCount']
        options = {
            'pdf': {
                'FilterName': 'writer_pdf_Export',
                'FilterData': {
                    'PageRange': {
                        'type': 'range',
                        'label': 'Pages Range',
                        'min': 1,
                        'max': pageCount
                    },
                    'UseLosslessCompression': {
                        'type': 'boolean',
                        'label': 'Use Lossless Compression',
                        'default': True
                    },
                    'Quality': {
                        'type': 'slide',
                        'label': 'Quality, %',
                        'min': 1,
                        'max': 100,
                        'default': 90
                    },
                    'MaxImageResolution': {
                        'type': 'select',
                        'label': 'Max Image Resolution',
                        'options': {
                            75: '75 DPI',
                            150: '150 DPI',
                            300: '300 DPI',
                            600: '600 DPI',
                            1200: '1200 DPI'
                        },
                        'default': 150
                    },
                    'EmbedStandardFonts': {
                        'type': 'boolean',
                        'label': 'Embed Standard Fonts',
                        'default': False
                    },
                    'Watermark': {
                        'type': 'string',
                        'label': 'Watermark',
                        'default': ''
                    },
                    'InitialView': {
                        'type': 'select',
                        'label': 'Initial View',
                        'options': {
                            0: 'Viewer Mode',
                            1: 'With Outline Pane',
                            2: 'With Thumbnail Pane'
                        },
                        'default': 2
                    },
                    'ResizeWindowToInitialPage': {
                        'type': 'boolean',
                        'label': 'Resize to Initial',
                        'default': False
                    }
                }
            },
            'odt': {
                'FilterName': 'writer8',
                'FilterData': {}
            },
            'doc': {
                'FilterName': 'MS Word 97',
                'FilterData': {}
            },
            'jpg': {
                'FilterName': 'draw_jpg_Export',
                'FilterData': {}
            },
            'png': {
                'FilterName': 'draw_png_Export',
                'FilterData': {}
            },
            'tiff': {
                'FilterName': 'draw_tif_Export',
                'FilterData': {}
            }
            # // "draw_pdf_Export", "draw_svg_Export"
        }
        if extension is None or not extension in options:
            return options
        return options[extension]