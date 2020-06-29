## ABAP Helpers

Three remote enabled ABAP Function Modules (RFM) are required in ABAP backend, any system/release.

:exclamation: Implementations given here are just an example, neither maintained, nor supported in this repository

- **FTLS_DOMVALUES_GET** returns ABAP DOMAIN values, Search Help type F

- **FTLS_SHLP_METADATA_GET** returns ABAP F4 Search Help metadata, to be consumed by Value Input Help frontend search form generator

- **FTLS_SHLP_GET** returns the F4 Search Help result, based on frontend serch form input values

| RFM                    | Design-time | Run-time           | Using internally                                                          |
| ---------------------- | ----------- | ------------------ | ------------------------------------------------------------------------- |
| FTLS_DOMVALUES_GET     |             | :white_check_mark: | DD_DOMVALUES_GET                                                          |
| FTLS_SHLP_METADATA_GET |             | :white_check_mark: | FTLS_SHLP_METADATA_GET<br/>F4TOOL_GET_DEF_SHLP<br/>F4IF_EXPAND_SEARCHHELP |
| FTLS_SHLP_GET          |             | :white_check_mark: | F4IF_GET_SHLP_DESCR<br/>F4IF_SELECT_VALUES                                |
