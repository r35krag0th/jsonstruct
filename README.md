jsonstruct
==========

jsonstruct is a library for two way conversion of typed Python object and JSON. This project is originally a fork of [jsonpickle](jsonpickle.github.com) (Thanks guys!).

The key difference between this library and jsonpickle is that during deserialization, jsonpickle requires Python types to be specified as part of the JSON. This library intend to remove this requirement, and instead, allows you to specify the class that it will be deserialized into. It will exam the class definiton and create a typed Python object as a result. This approach is similar to how [Jackson](https://github.com/FasterXML/jackson) works.
    
    import jsonstruct

    # Create sample classes
    class Address(object):
        city = ""
        province = ""


    class Developer(object):
        name = ""
        title = ""
        address = Address()
        safe_houses = [Address()]           # Indicates a list of Addresses.
        work_locations = {"": Address()}    # Indicates a dict of Addresses.
        language_set = set([""])            # Indicates a set of str.


    d = Developer()
    d.name = "Bob"
    d.title = "Developer"
    d.address = Address()
    d.address.city = "Toronto"
    d.address.province = "Ontario"

    d.safe_houses = [Address(), Address()]
    d.safe_houses[0].city = "Secret"
    d.safe_houses[1].city = "Middle of nowhere"

    d.work_locations = {"Company": Address()}
    d.work_locations["Company"].city = "Markham"
    d.work_locations["Company"].province = "Ontario"

    d.language_set = set(["en", "fr"])

    j = jsonstruct.encode(d)
    print j         # {"name": "Bob", "title": "Developer",
                    # "work_locations":
                    # {"Company": {"province": "Ontario", "city": "Markham"}},
                    # "address": {"province": "Ontario", "city": "Toronto"},
                    # "language_set": ["fr", "en"],
                    # "safe_houses":
                    # [{"city": "Secret"}, {"city": "Middle of nowhere"}]}

    e = jsonstruct.decode(j, Developer)

    print e.name    # Bob
    print e.title   # Developer
    print e.address.city        # Toronto
    print e.safe_houses[0].city # Secret
    print e.safe_houses[1].city # Middle of nowhere
    print e.work_locations["Company"].city      # Markham
    print e.work_locations["Company"].province  # Ontario
    print e.language_set        # set([u'fr', u'en'])

    # By default the encoder will filter out any attributes with None value;
    # in case the unmarshaller doesn't like having null value assigned on
    # primitive types (Jackson is fine though).
    a = Address()
    a.city = "Toronto"
    a.province = None

    print jsonstruct.encode(a)  # {"city": "Toronto"}

    # However this behaviour can be overridden with
    # is_filter_none_attr = False argument on encode().

    print jsonstruct.encode(a, is_filter_none_attr = False)
    # {"province": null, "city": "Toronto"}

The purpose of this library is allow creating typed RESTful web services or clients, where data schema need to be defined and shared between client and server. It is also not ideal to expect incoming or outgoing JSON request or response to contain Python types as part of the JSON. Data types needed for services could sometimes grow very complex, making schema/type definition much more important and easier to understand.

Please note that this due to the duct-typing nature of Python, when constructing data, it's still up to you to ensure that you follow your own schema. This library currently does not have a feature to validate schema of data during encoding. It should be possible and would make sense to have such a feature. If anyone wants to contribute such feature, please let me know. Also note that this library supports very simple and straight forward schema definition and it does not support sophisticated, XSD style validation. If you are interested in more sophistication, please look into [Colander](http://docs.pylonsproject.org/projects/colander/en/latest/), [limone](https://pypi.python.org/pypi/limone) or [pyxb](http://pyxb.sourceforge.net/)

This project is licensed under BSD License. Please see COPYING

**This library pretty much ready. Please help testing it.**

