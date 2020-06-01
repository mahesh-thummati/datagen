---
title: 'DataGen - Synthesize your data'
---

This module can be used directly from command line with command
\"datagen\" after it is installed or can be used as part of python code.

It\'s main purpose is to generate fake data based on user provided json
config file.

When invoked from command line:

:   

    **mandatory arguments**

    :   action: valid values are execute/validate

        inp\_json: input config json file

    **examples**

    :   \$datagen validate config.json

        Input json file is valid.

        \$datagen execute \~/test.json \--quiet

        Data generated successfully.

The json file follows a specific structure as outlined below.

It has following names which are used to control the number of records
to be written, type of output file format, seed to reproduce data and
output file name.

**name**

:   Name of the datagen instance.

**output\_format**

:   Output format to save the file, valid values are parquet and csv.

**output\_rec\_cnt**

:   Number of records to be generated.

**source**

:   Source of the data source, valid value is \"fake\" for now.

**seed**

:   Any int value for reproducible results.

**output\_file**

:   Output file name, can be in local file system or s3 bucket.

**fields**

:   List of fields to generate.

    Each field has its own set of named types that drives how data is
    generated. Following are the valid list of named types.

    **name**

    :   Name of the field.

    **type**

    :   Data type of the field. Below are the list of valid data types.
        Depending on the data type a few extra elements can be added to
        control how the data is generated.

        **address**

        :   Generates a random USA address in format
            \'{street\_address}n{city}, {state\_abbr} {postcode}\'.

        **boolean**

        :   Boolean data type, generates random boolean data.

        **cat**

        :   Catogorical data type, randomly selects a value from a list
            of provided *values*.

        **city**

        :   Generates a random city in the USA.

        **country**

        :   Generates a random country.

        **currency\_code**

        :   Generates a random three letter currency code.

        **currency\_name**

        :   Generates a random currency name.

        **date**

        :   Data data type, generates any date between 1970-01-01 and
            now by defaul. Can be controlled with *min\_value* and
            *max\_value*. Date format is %Y-%m-%d.

        **decimal**

        :   Decimal data type, generates random decimal value. Can be
            controlled with *min\_value* and *max\_value*.

        **double**

        :   Double data type, generates random double value. Can be
            controlled with *min\_value* and *max\_value*.

        **float**

        :   Float data type, generates random float value. Can be
            controlled with *min\_value* and *max\_value*.

        **first\_name**

        :   Generates a random first name.

        **int**

        :   Int data type, generates random int value. Can be controlled
            with *min\_value* and *max\_value*.

        **job**

        :   Generates a random profession.

        **last\_name**

        :   Generates a random last name.

        **lorem**

        :   Gnerates lorem ipsum random text, can be contolled with
            *max\_length*/*values*. While *max\_length* controlls the
            number of sentences to be in the paragraph, *values* can be
            used to provide list of words to use instead of ipsum.

        **name**

        :   Generates a fake name.

        **state**

        :   Generates a random US state.

        **str**

        :   String data type, randomly generates a string of 20
            characters by default. Can be controlled with *min\_lenght*
            and *max\_lenght* or using *format*. Use following
            characters to control the format of the field, for example
            format \"Datagen - ??\#\#\#\#\" will generate random
            \'Datagen - aZ0873\'.

            -   Question marks (\'?\') are replaced with a random letter
                (a-zA-Z)
            -   Number signs ('\#') are replaced with a random digit (0
                to 9).
            -   Percent signs ('%') are replaced with a random non-zero
                digit (1 to 9).
            -   Exclamation marks ('!') are replaced with a random digit
                or an empty string.
            -   At symbols ('@') are replaced with a random non-zero
                digit or an empty string.

        **street\_address**

        :   Generates a random USA street address.

        **time**

        :   Time data type, generates any timestamp between -30years and
            now by default. Can be controlled with *min\_value* and
            *max\_value*. Timestamp format is %Y-%m-%d %H:%M:%S.

        **timestamp**

        :   Timestamp data type, generates any timestamp between
            -30years and now by default. Can be controlled with
            *min\_value* and *max\_value*. Timestamp format is %Y-%m-%d
            %H:%M:%S.

        **zip\_code**

        :   Generates a random USA zipcode.

    **min\_length**

    :   Min length of a field.

    **max\_length**

    :   Max length of a field.

    **min\_value**

    :   Min value to generate for a field.

    **max\_value**

    :   Max value to generate for a field.

    **values**

    :   List of values to choose from.

    **format**

    :   Format of the string to generate.
