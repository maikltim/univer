declare variable $doc := doc("store.xml");
<html>
    <body>
        <h2>Ассортимент компьютерной техники</h2>
        <table border="1">
            <tr>
                <th>№</th>
                <th>ID</th>
                <th>Название</th>
                <th>Категория</th>
                <th>Цена</th>
                <th>На складе</th>
            </tr>
            {
                for $product at $pos in $doc/store/products/product
                order by $product/price descending
                return
                    <tr>
                        <td>{$pos}</td>
                        <td>{$product/@id}</td>
                        <td>{$product/name}</td>
                        <td>{$product/@category}</td>
                        <td>{$product/price}</td>
                        <td>{$product/stock}</td>
                    </tr>
            }
        </table>
    </body>
</html>