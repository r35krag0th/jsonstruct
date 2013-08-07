jsonstruct
==========

jsonstruct is a library for two way conversion of typed Python object and JSON. This project is originally a fork of [jsonpickle](jsonpickle.github.com) (Thanks guys!).

The key difference between this library and jsonpickle is that during deserialization, jsonpickle requires Python types to be specified as part of the JSON. This library intend to remove this requirement, and instead, allows you to specify the class that it will be deserialized into. It will exam the class definiton and create a typed Python object as a result. This approach is similar to how [Jackson](https://github.com/FasterXML/jackson) works.
    
    import jsonstruct

    class Address(object):
        city = ""
        province = ""


    # Create sample types
    class Test(object):
        name = ""
        title = ""
        address = Address()
        safe_houses = [Address()]   # This indicates a list of Address.


    t = Test()
    t.name = "Alice"
    t.title = "Developer"
    t.address = Address()
    t.address.city = "Toronto"
    t.address.province = "Ontario"

    t.safe_houses = [Address(), Address()]
    t.safe_houses[0].city = "Waterloo"
    t.safe_houses[1].city = "Middle of nowhere"

    j = jsonstruct.encode(t)
    print j         # '{"title": "Developer", "name": "Alice", "safe_houses": [{"city": "Waterloo"}, {"city": "Middle of nowhere"}], "address": {"province": "Ontario", "city": "Toronto"}}'

    u = jsonstruct.decode(j, Test)

    print u.name    # 'Alice'
    print u.title   # 'Developer'
    print u.address.city        # 'Toronto'
    print u.safe_houses[0].city # 'Waterloo'
    print u.safe_houses[1].city # 'Middle of nowhere'

The purpose of this library is allow creating typed RESTful web services or clients, where data schema need to be defined and shared between client and server. It is also not ideal to expect incoming or outgoing JSON request or response to contain Python types as part of the JSON. Data types needed for services could sometimes grow very complex, making schema/type definition much more important and easier to understand.

Please note that this due to the duct-typing nature of Python, when constructing data, it's still up to you to ensure that you follow your own schema. This library currently does not have a feature to validate schema of data during encoding. It should be possible and would make sense to have such a feature. If anyone wants to contribute such feature, please let me know. Also note that this library supports very simple and straight forward schema definition and it does not support sophisticated, XSD style validation. If you are interested in more sophistication, please look into [Colander](http://docs.pylonsproject.org/projects/colander/en/latest/), [limone](https://pypi.python.org/pypi/limone) or [pyxb](http://pyxb.sourceforge.net/)

This project is licensed under BSD License. Please see COPYING

**This library is currently at a very immature stage. Please help testing it out.**

