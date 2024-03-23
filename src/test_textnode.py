import unittest

from textnode import (
    TextNode,
    split_nodes_images,
    split_nodes_links,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html_node,
    split_nodes_delimeter,
    extract_markdown_images,
    extract_markdown_links
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold", "http://example.com")
        self.assertEqual(text_node_1, text_node_2)
        
    def test_eq_none(self):
        text_node_1 = TextNode("Test", "bold")
        text_node_2 = TextNode("Test", "bold")
        self.assertEqual(text_node_1, text_node_2)
        
    def test_ne(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold", "http://example.org")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_text(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test2", "bold", "http://example.com")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_text_type(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "italic", "http://example.com")
        self.assertNotEqual(text_node_1, text_node_2)
        
    def test_ne_none(self):
        text_node_1 = TextNode("Test", "bold", "http://example.com")
        text_node_2 = TextNode("Test", "bold")
        self.assertNotEqual(text_node_1, text_node_2)
        
        
class TestTextNodeToHTML(unittest.TestCase):       
    def test_text_node_to_html(self):
        text_node = TextNode(text="test", text_type=text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_bold(self):
        text_node = TextNode(text="test", text_type=text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_italic(self):
        text_node = TextNode(text="test", text_type=text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_code(self):
        text_node = TextNode(text="test", text_type=text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, text_node.text)
        
    def test_text_node_to_html_link(self):
        text_node = TextNode(text="test", text_type=text_type_link, url="http://ur.l")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, text_node.text)
        self.assertDictEqual(html_node.props, {"href": text_node.url})
        
    def test_text_node_to_html_image(self):
        text_node = TextNode(text="test", text_type=text_type_image, url="http://ur.l")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": text_node.url, "alt": text_node.text})
        
    def test_text_node_to_html_unknown_type(self):
        text_node = TextNode(text="test", text_type="unknown")
        self.assertRaises(ValueError, text_node_to_html_node, text_node)
        
        
class TestSplitNodesDelimeter(unittest.TestCase):
    def test_split_nodes_delimeter_bold(self):
        text_node = TextNode(text="This is **bold** text", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[2].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text, "bold")
        
    def test_split_nodes_delimeter_two_bold(self):
        text_node = TextNode(text="This is **bold** and **this** is too", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 5)
        for index, node in enumerate(new_nodes):
            if index % 4 == 0:
                self.assertEqual(node.text_type, text_type_text)
                self.assertEqual(len(node.text.split(" ")), 3) # 3 because of trailing whitespace
            elif index % 2 != 0:
                self.assertEqual(node.text_type, text_type_bold)
                self.assertEqual(len(node.text.split(" ")), 1)
                
    def test_split_nodes_delimeter_at_end_of_text(self):
        text_node = TextNode(text="This is **bold**", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text, "bold")
        
    def test_split_nodes_delimeter_at_start_of_text(self):
        text_node = TextNode(text="**bold** this is", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[1].text_type, text_type_text)
        self.assertEqual(new_nodes[0].text_type, text_type_bold)
        self.assertEqual(new_nodes[0].text, "bold")
                
    def test_split_nodes_delimeter_no_bold(self):
        text_node = TextNode(text="This is *italic* text", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        
    def test_split_nodes_delimeter_no_italic(self):
        text_node = TextNode(text="This is **not** italic", text_type=text_type_text)
        self.assertRaises(RuntimeError, split_nodes_delimeter, old_nodes=[text_node], delimeter="*", text_type=text_type_italic)
        
    def test_split_nodes_delimeter_italic(self):
        text_node = TextNode(text="This is *italic* text", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '*', text_type_italic)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[2].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_italic)
        self.assertEqual(new_nodes[1].text, "italic")
        
    def test_split_nodes_delimeter_code(self):
        text_node = TextNode(text="This is `code`", text_type=text_type_text)
        new_nodes = split_nodes_delimeter([text_node], '`', text_type_code)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_code)
        self.assertEqual(new_nodes[1].text, "code")
        
    def test_split_nodes_delimeter_not_text_type(self):
        text_node = TextNode(text="This is **bold** text", text_type=text_type_text)
        text_node_bold = TextNode(text="This is **bold**", text_type=text_type_bold)
        new_nodes = split_nodes_delimeter([text_node, text_node_bold], '**', text_type_bold)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text_type, text_type_text)
        self.assertEqual(new_nodes[2].text_type, text_type_text)
        self.assertEqual(new_nodes[1].text_type, text_type_bold)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[3].text_type, text_type_bold)
        self.assertEqual(new_nodes[3].text, "This is **bold**")
        
class TestExtractMarkdownImages(unittest.TestCase):
    def test_one_image(self):
        raw_text = "This is an image: ![alt_text](https://url.url)"
        images = extract_markdown_images(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt_text", "https://url.url"))
        
    def test_two_images(self):
        raw_text = "This is an image: ![alt_text](https://url.url) and this is too: ![alt_text_too](https://url_too.url)"
        images = extract_markdown_images(raw_text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("alt_text", "https://url.url"))
        self.assertEqual(images[1], ("alt_text_too", "https://url_too.url"))
        
    def test_alt_text_containing_parenthesis(self):
        raw_text = "This is an image: ![an (alternative) text](https://url.url)"
        images = extract_markdown_images(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("an (alternative) text", "https://url.url"))
        
    def test_url_containing_sq_brackets(self):
        raw_text = "This is an image: ![alt_text](https://url.url/5[tq)"
        images = extract_markdown_images(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt_text", "https://url.url/5[tq"))
        
    def test_raw_text_containing_link(self):
        raw_text = "This is an image: ![alt_text](https://url.url) and this is a link: [text](https://url.url)"
        images = extract_markdown_images(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt_text", "https://url.url"))
        
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_one_link(self):
        raw_text = "This is a link: [text](https://url.url)"
        images = extract_markdown_links(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("text", "https://url.url"))
        
    def test_two_link(self):
        raw_text = "This is a link: [text](https://url.url) and this is too: [text_too](https://url_too.url)"
        images = extract_markdown_links(raw_text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("text", "https://url.url"))
        self.assertEqual(images[1], ("text_too", "https://url_too.url"))
        
    def test_text_containing_parenthesis(self):
        raw_text = "This is a link: [an (alternative) text](https://url.url)"
        images = extract_markdown_links(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("an (alternative) text", "https://url.url"))
        
    def test_url_containing_sq_brackets(self):
        raw_text = "This is a link: [text](https://url.url/5[tq)"
        images = extract_markdown_links(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("text", "https://url.url/5[tq"))
        
    def test_raw_text_containing_image(self):
        raw_text = "This is an image: ![alt_text](https://url.url) and this is a link: [text](https://url.url)"
        images = extract_markdown_links(raw_text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("text", "https://url.url"))
        
        
class TestSlitNodesImages(unittest.TestCase):
    def test_one_image(self):
        text_node = TextNode("This is an image: ![alt_text](https://image.url)", text_type_text)
        image_nodes = split_nodes_images([text_node])
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].text, "This is an image: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text, "alt_text")
        self.assertEqual(image_nodes[1].text_type, text_type_image)
        self.assertEqual(image_nodes[1].url, "https://image.url")
        
    def test_two_images(self):
        text_node = TextNode("This is an image: ![alt_text](https://image.url), and this is another: ![alt_text1](https://image1.url)", text_type_text)
        image_nodes = split_nodes_images([text_node])
        self.assertEqual(len(image_nodes), 4)
        self.assertEqual(image_nodes[0].text, "This is an image: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[2].text, ", and this is another: ")
        self.assertEqual(image_nodes[2].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text_type, text_type_image)
        self.assertEqual(image_nodes[3].text_type, text_type_image)
        
    def test_one_image_one_link(self):
        text_node = TextNode("This is an image: ![alt_text](https://image.url), and this is a link: [text1](https://link.url)", text_type_text)
        image_nodes = split_nodes_images([text_node])
        self.assertEqual(len(image_nodes), 3)
        self.assertEqual(image_nodes[0].text, "This is an image: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[2].text, ", and this is a link: [text1](https://link.url)")
        self.assertEqual(image_nodes[2].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text_type, text_type_image)
        
    def test_one_image_no_prefix(self):
        text_node = TextNode("![alt_text](https://image.url), and that was an image", text_type_text)
        image_nodes = split_nodes_images([text_node])
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].text, "alt_text")
        self.assertEqual(image_nodes[0].text_type, text_type_image)
        self.assertEqual(image_nodes[0].url, "https://image.url")
        self.assertEqual(image_nodes[1].text, ", and that was an image")
        self.assertEqual(image_nodes[1].text_type, text_type_text)
        
    def test_no_images(self):
        text_node = TextNode("This text contains no images", text_type_text)
        image_nodes = split_nodes_images([text_node])
        self.assertEqual(len(image_nodes), 1)
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[0].text, "This text contains no images")


class TestSlitNodesLinks(unittest.TestCase):
    def test_one_link(self):
        text_node = TextNode("This is a link: [text](https://link.url)", text_type_text)
        image_nodes = split_nodes_links([text_node])
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].text, "This is a link: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text, "text")
        self.assertEqual(image_nodes[1].text_type, text_type_link)
        self.assertEqual(image_nodes[1].url, "https://link.url")
        
    def test_two_links(self):
        text_node = TextNode("This is a link: [text](https://link.url), and this is another: [text1](https://link1.url)", text_type_text)
        image_nodes = split_nodes_links([text_node])
        self.assertEqual(len(image_nodes), 4)
        self.assertEqual(image_nodes[0].text, "This is a link: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[2].text, ", and this is another: ")
        self.assertEqual(image_nodes[2].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text_type, text_type_link)
        self.assertEqual(image_nodes[3].text_type, text_type_link)
        
    def test_one_link_one_image(self):
        text_node = TextNode("This is a link: [text](https://link.url), and this is an image: ![alt_text](https://image.url)", text_type_text)
        image_nodes = split_nodes_links([text_node])
        self.assertEqual(len(image_nodes), 3)
        self.assertEqual(image_nodes[0].text, "This is a link: ")
        self.assertEqual(image_nodes[0].text_type, text_type_text)
        self.assertEqual(image_nodes[2].text, ", and this is an image: ![alt_text](https://image.url)")
        self.assertEqual(image_nodes[2].text_type, text_type_text)
        self.assertEqual(image_nodes[1].text_type, text_type_link)
        
    def test_one_image_no_prefix(self):
        text_node = TextNode("[text](https://link.url), and that was a link", text_type_text)
        image_nodes = split_nodes_links([text_node])
        self.assertEqual(len(image_nodes), 2)
        self.assertEqual(image_nodes[0].text, "text")
        self.assertEqual(image_nodes[0].text_type, text_type_link)
        self.assertEqual(image_nodes[0].url, "https://link.url")
        self.assertEqual(image_nodes[1].text, ", and that was a link")
        self.assertEqual(image_nodes[1].text_type, text_type_text)
        
        
if __name__ == "__main__":
    unittest.main()