import shopify
from test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource.util import xml_to_dict

class OrderTest(TestCase):

    def test_should_be_loaded_correctly_from_order_xml(self):
        order_xml = """<?xml version="1.0" encoding="UTF-8"?>
          <order>
            <note-attributes type="array">
              <note-attribute>
                <name>size</name>
                <value>large</value>
              </note-attribute>
            </note-attributes>
          </order>"""
        order = shopify.Order(xml_to_dict(order_xml)["order"])

        self.assertEqual(1, len(order.note_attributes))

        note_attribute = order.note_attributes[0]
        self.assertEqual("size", note_attribute.name)
        self.assertEqual("large", note_attribute.value)

    def test_should_be_able_to_add_note_attributes_to_an_order(self):
        order = shopify.Order()
        order.note_attributes = []
        order.note_attributes.append(shopify.NoteAttribute({'name': "color", 'value': "blue"}))

        order_xml = xml_to_dict(order.to_xml())
        note_attributes = order_xml["order"]["note_attributes"]
        self.assertTrue(isinstance(note_attributes, list))

        attribute = note_attributes[0]
        self.assertEqual("color", attribute["name"])
        self.assertEqual("blue", attribute["value"])
