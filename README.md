# 4chan API Schema

This respository contains [JSON schemas](http://json-schema.org/) that can validate 4chan's API, and, more importantly, describe its structure in detail.

The JSON schema files were initially based on 4chan's [official API documentation](https://github.com/4chan/4chan-API), but have been updated to conform with actual API data structures encountered.  They will also be used as the basis for for more extensive documentation.

# Why?

The 4chan API documentation is woefully out of date, as well as inaccurate.  In addition, data from the actual 4chan API can occasionally be received in a broken, yet well-formed state.  As someone developing an archival bot and search engine, the need for a way to verify the structure of API structures is paramount.

# Usage

The JSON Schema files are under `v1.0` and have `.json_schema` as their file extension.  They use Draft 4 of the JSON schema.  Simply validate your JSON against the appropriate schema to check its structure.

# License

These files are &copy;2015 Rob "N3X15" Nelson and are licensed under the MIT Open-Source License.

See [LICENSE](LICENSE) for more information.

Enjoy.

# Support

Inaccuracies can be reported in the GitHub issues panel.

All other support will not be available.
