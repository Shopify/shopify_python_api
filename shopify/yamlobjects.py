try:
    # Shopify serializes receipts in YAML format, and yaml.safe_load will
    # not automatically load custom types because of security purpose,
    # so create safe loaders for types returned from Shopify here.
    #
    # The YAMLObject metaclass will automatically add these classes to
    # the list of constructors for yaml.safe_load to use.
    import yaml

    class YAMLHashWithIndifferentAccess(yaml.YAMLObject):
        yaml_tag = "!map:ActiveSupport::HashWithIndifferentAccess"
        yaml_loader = yaml.SafeLoader

        @classmethod
        def from_yaml(cls, loader, node):
            return loader.construct_mapping(node, cls)

except ImportError:
    pass
