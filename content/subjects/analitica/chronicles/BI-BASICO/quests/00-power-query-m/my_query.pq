// Operator workspace for Quest BI-00
// Paste your exported Power Query M script from Advanced Editor below.
let
    Source = Csv.Document(
        File.Contents("C:\path\to\faro_sales_raw.csv"),
        [Delimiter = ",", Columns = 9, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
    // TODO: Add RenamedColumns, TypedTable, FilteredRows, and CleanedText steps
in
    PromotedHeaders
