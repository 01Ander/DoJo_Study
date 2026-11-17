// Reference Power Query (M) script for Quest BI-00 (Libreria El Faro)
let
    Source = Csv.Document(
        File.Contents("C:\path\to\faro_sales_raw.csv"),
        [Delimiter = ",", Columns = 9, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    RenamedColumns = Table.RenameColumns(
        PromotedHeaders,
        {
            {"id_venta", "sale_id"},
            {"fecha_venta", "sale_date"},
            {"tienda_id", "store_id"},
            {"tienda_nombre", "store_name"},
            {"unidades", "units"},
            {"precio_unitario", "unit_price"},
            {"costo_unitario", "unit_cost"},
            {"monto_cop", "amount_cop"},
            {"estado", "order_status"}
        }
    ),
    TypedTable = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {"sale_id", type text},
            {"sale_date", type date},
            {"store_id", type text},
            {"store_name", type text},
            {"units", Int64.Type},
            {"unit_price", Int64.Type},
            {"unit_cost", Int64.Type},
            {"amount_cop", Int64.Type},
            {"order_status", type text}
        }
    ),
    FilteredRows = Table.SelectRows(
        TypedTable,
        each [sale_id] <> null and [sale_id] <> "" and [order_status] <> "cancelled"
    ),
    CleanedText = Table.TransformColumns(
        FilteredRows,
        {
            {"store_name", each Text.Upper(Text.Trim(_)), type text}
        }
    )
in
    CleanedText
