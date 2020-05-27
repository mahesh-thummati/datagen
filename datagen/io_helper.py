import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from s3fs.core import S3FileSystem

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class IOException(Error):
    pass

class IOHelper:
    """This Class helps with IO operations."""
    
    def __init__(self, profile_name="default"):
        self.profile_name = profile_name
    
    def _determite_file_system(self, filename):
        """Determines file system
        Args:
            filename: filename to determine file system
        Returns:
            returns s3 if file system is s3, else None
        """
        if filename.startswith("s3://"):
            s3 = S3FileSystem(anon=False, profile_name=self.profile_name)
            return s3
        else:
            return None
    
    def read_parquet(self, input_location, columns=None, read_dictionary=None):
        """Reads parquet file as pandas dataframe.
        Args:
            input_location: location of input parquet file
            columns: list of columns to read if interested in only a few columns
            read_dictionary: list of columns to read as catagorical variables
        Returns: 
            Pandas Dataframe
        Raises:
            IOException if parquet files cannot be read/converted to pandas df
        """
        try:
            table = pq.read_table(source=input_location, columns=columns,
                read_dictionary=read_dictionary, use_pandas_metadata=True,
                filesystem=self._determite_file_system(input_location))
        except Exception as e:
            raise IOException("Cann't read parquet file, exception {0} occurred.".format(e))
        try:
            df = table.to_pandas()
        except Exception as e:
            raise IOException("Cann't convert parquet file into pandas df, exception {0} occurred.".format(e))
        return df
    
    def write_as_csv(self, dataframe_to_persist, output_location, **kwargs):
        """ Persists pandas dataframe as csv file. 
        Args:
            dataframe_to_persist: pandas data frame to persist as csv file
            output_location: output file location, can be s3/local file system
            kwargs: dict of parameters that will be passed to pandas to_csv
        Returns:
            status of write operation
        Raises:
            IOException if df cann't be persisted as csv
        """
        filesystem = self._determite_file_system(output_location)
        try:
            if isinstance(filesystem, S3FileSystem):
                with filesystem.open(output_location,'w') as f:
                    dataframe_to_persist.to_csv(f, **kwargs)
            else:
                dataframe_to_persist.to_csv(output_location, **kwargs)
        except Exception as e:
            raise IOException("Cann't persist dataframe as csv, exception {0} occurred.".format(e))
        return True
    
    def write_as_parquet(self, dataframe_to_persist, output_location, index=False,
        compression="snappy", coerce_timestamps="ms", flavor="spark", version="1.0",
        allow_truncated_timestamps=True, use_deprecated_int96_timestamps=True):
        """Persists pandas dataframe as parquet file. 
        Args:
            dataframe_to_persist: pandas df to persist
            output_location: file name to write
            index: whether to include pandas df index in the output file
            compression: algorithm to use to compress parquet file.
                         valid values - ‘NONE’, ‘SNAPPY’, ‘GZIP’, ‘LZO’, ‘BROTLI’, ‘LZ4’, ‘ZSTD’
            coerce_timestamps: set timestamps precision, valid values - ms, us
            allow_truncated_timestamps: whether to truncate timestamps if lower level precison is chosen above
            flavor: sanitize schema to work with other systems
            use_deprecated_int96_timestamps: set this to true if parquet files are read from impala/spark
        Returns:
            status of write operation
        Raises:
            IOException if df cann't be persisted as parquet
        """
        table = pa.Table.from_pandas(dataframe_to_persist, preserve_index=index)
        try:
            pq.write_table(
                table=table,
                where=output_location,
                filesystem=self._determite_file_system(output_location),
                compression=compression,
                coerce_timestamps=coerce_timestamps,
                allow_truncated_timestamps=allow_truncated_timestamps,
                version=version,
                flavor=flavor,
                use_deprecated_int96_timestamps=use_deprecated_int96_timestamps
            )
        except Exception as e:
            raise IOException("Cann't persist dataframe as parquet, exception {0} occurred.".format(e))
        return True