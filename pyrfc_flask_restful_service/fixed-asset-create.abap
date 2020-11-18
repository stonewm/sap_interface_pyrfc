REPORT  zaa_create.

DATA: ls_key TYPE bapi1022_key,
      ls_general_data TYPE bapi1022_feglg001,
      ls_general_data_x TYPE bapi1022_feglg001x,
      ls_time_dependent_data TYPE bapi1022_feglg003,
      ls_time_dependent_data_x TYPE bapi1022_feglg003x,
      ls_asset TYPE bapi1022_1-assetmaino,
      ls_return TYPE bapiret2.

* key
ls_key-companycode = 'Z900'.

* general data
ls_general_data-assetclass = 'Z060'.
ls_general_data-descript = 'HW企业智慧屏IdeaHub'.

ls_general_data_x-assetclass = 'X'.
ls_general_data_x-descript = 'X'.

* time dependent data
ls_time_dependent_data-costcenter = 'Z90020'.
ls_time_dependent_data_x-costcenter = 'X'.

CALL FUNCTION 'BAPI_FIXEDASSET_CREATE1'
  EXPORTING
    key                = ls_key
    generaldata        = ls_general_data
    generaldatax       = ls_general_data_x
    timedependentdata  = ls_time_dependent_data
    timedependentdatax = ls_time_dependent_data_x
  IMPORTING
    asset              = ls_asset
    return             = ls_return.


IF ls_asset IS NOT INITIAL.
  CALL FUNCTION 'BAPI_TRANSACTION_COMMIT' .
  WRITE: / '资产:',ls_asset, '已成功创建.'.
ELSE.
  CALL FUNCTION 'BAPI_TRANSACTION_ROLLBACK' .
ENDIF.