REPORT  z_table_to_txt.

DATA: gt_zemployee TYPE STANDARD TABLE OF zemployee,
      gs_zemployee LIKE LINE OF gt_zemployee.

DATA: file_name TYPE string VALUE '.\zemp.dat'.

DATA: line TYPE string.

START-OF-SELECTION.
  DELETE DATASET file_name.

  OPEN DATASET file_name FOR APPENDING IN TEXT MODE ENCODING DEFAULT WITH WINDOWS LINEFEED.

  SELECT * FROM zemployee
    INTO CORRESPONDING FIELDS OF TABLE gt_zemployee PACKAGE SIZE 1000.

    LOOP AT gt_zemployee INTO gs_zemployee.
      CONCATENATE gs_zemployee-empid gs_zemployee-empname gs_zemployee-empaddr gs_zemployee-phone
           INTO line SEPARATED BY ','.
      TRANSFER line TO file_name NO END OF LINE.
    ENDLOOP.
    CLEAR gt_zemployee[].
  ENDSELECT.

  CLOSE DATASET file_name.

  WRITE 'Zemployee table downloaded successfully.'.