#!/usr/bin/python

class FilterModule(object):
    def filters(self):
        return {
            'tag_images': self.do_tag_images
        }

    def do_tag_images(self, definitions, tag):
      ee_list = []
      for ee_name in definitions.keys():
        definitions[ee_name]['tag'] = tag
        ee_list.append(definitions[ee_name])
      return ee_list