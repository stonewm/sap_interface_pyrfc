FUNCTION zfm_as01.
*"----------------------------------------------------------------------
*"*"Local Interface:
*"  IMPORTING
*"     VALUE(CTU) LIKE  APQI-PUTACTIVE DEFAULT 'X'
*"     VALUE(MODE) LIKE  APQI-PUTACTIVE DEFAULT 'N'
*"     VALUE(UPDATE) LIKE  APQI-PUTACTIVE DEFAULT 'L'
*"     VALUE(GROUP) LIKE  APQI-GROUPID OPTIONAL
*"     VALUE(USER) LIKE  APQI-USERID OPTIONAL
*"     VALUE(KEEP) LIKE  APQI-QERASE OPTIONAL
*"     VALUE(HOLDDATE) LIKE  APQI-STARTDATE OPTIONAL
*"     VALUE(NODATA) LIKE  APQI-PUTACTIVE DEFAULT '/'
*"     VALUE(ANLKL) LIKE  BDCDATA-FVAL DEFAULT 'Z060'
*"     VALUE(BUKRS) LIKE  BDCDATA-FVAL DEFAULT 'Z900'
*"     VALUE(NASSETS) LIKE  BDCDATA-FVAL DEFAULT '1'
*"     VALUE(TXT50) LIKE  BDCDATA-FVAL DEFAULT '固定资产名称'
*"     VALUE(MEINS) LIKE  BDCDATA-FVAL DEFAULT 'EA'
*"     VALUE(KOSTL) LIKE  BDCDATA-FVAL DEFAULT 'Z90020'
*"  EXPORTING
*"     VALUE(SUBRC) LIKE  SYST-SUBRC
*"  TABLES
*"      MESSTAB STRUCTURE  BDCMSGCOLL OPTIONAL
*"----------------------------------------------------------------------

  TABLES: t100.
  DATA: l_mstring(480).

  subrc = 0.

  PERFORM bdc_nodata      USING nodata.

  PERFORM open_group      USING group user keep holddate ctu.

  PERFORM bdc_dynpro      USING 'SAPLAIST'        '0105'.
  PERFORM bdc_field       USING 'BDC_OKCODE'      '/00'.
  PERFORM bdc_field       USING 'ANLA-ANLKL'      anlkl.
  PERFORM bdc_field       USING 'ANLA-BUKRS'      bukrs.
  PERFORM bdc_field       USING 'RA02S-NASSETS'   nassets.

  PERFORM bdc_dynpro      USING 'SAPLAIST'        '1000'.
  PERFORM bdc_field       USING 'BDC_OKCODE'      '=TAB02'.
  PERFORM bdc_field       USING 'ANLA-TXT50'      txt50.
  PERFORM bdc_field       USING 'ANLA-MEINS'      meins.

  PERFORM bdc_dynpro      USING 'SAPLAIST'        '1000'.
  PERFORM bdc_field       USING 'BDC_OKCODE'      '/00'.
  PERFORM bdc_field       USING 'ANLZ-KOSTL'      kostl.

  PERFORM bdc_dynpro      USING 'SAPLAIST'        '1000'.
  PERFORM bdc_field       USING 'BDC_OKCODE'      '=BUCH'.

  PERFORM bdc_transaction TABLES messtab
  USING                         'AS01'
                                ctu
                                mode
                                update.
  IF sy-subrc <> 0.
    subrc = sy-subrc.
    EXIT.
  ENDIF.

  LOOP AT messtab.
    SELECT SINGLE * FROM t100 WHERE sprsl = messtab-msgspra
                              AND   arbgb = messtab-msgid
                              AND   msgnr = messtab-msgnr.
    IF sy-subrc = 0.
      l_mstring = t100-text.
      IF l_mstring CS '&1'.
        REPLACE '&1' WITH messtab-msgv1 INTO l_mstring.
        REPLACE '&2' WITH messtab-msgv2 INTO l_mstring.
        REPLACE '&3' WITH messtab-msgv3 INTO l_mstring.
        REPLACE '&4' WITH messtab-msgv4 INTO l_mstring.
      ELSE.
        REPLACE '&' WITH messtab-msgv1 INTO l_mstring.
        REPLACE '&' WITH messtab-msgv2 INTO l_mstring.
        REPLACE '&' WITH messtab-msgv3 INTO l_mstring.
        REPLACE '&' WITH messtab-msgv4 INTO l_mstring.
      ENDIF.

      CONDENSE l_mstring.
      messtab-msgv1 = l_mstring.
      MODIFY messtab.
    ENDIF.

  ENDLOOP.

  PERFORM close_group USING     ctu.


ENDFUNCTION.

INCLUDE bdcrecxy .