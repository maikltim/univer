```xsl
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes"/>

    <!-- Шаблон для корневого элемента -->
    <xsl:template match="/SalesData">
        <DataWarehouse>
            <Facts>
                <!-- Удаление дубликатов по составному ключу: OrderID, ProductID -->
                <xsl:for-each select="Order[not(concat(OrderID, '|', ProductID) = preceding-sibling::Order/concat(OrderID, '|', ProductID))]">
                    <Fact>
                        <OrderID><xsl:value-of select="OrderID"/></OrderID>
                        <ProductID><xsl:value-of select="ProductID"/></ProductID>
                        <CustomerID><xsl:value-of select="CustomerID"/></CustomerID>
                        <OrderDate>
                            <xsl:choose>
                                <xsl:when test="OrderDate != ''">
                                    <xsl:value-of select="OrderDate"/>
                                </xsl:when>
                                <xsl:otherwise>0000-00-00</xsl:otherwise>
                            </xsl:choose>
                        </OrderDate>
                        <Amount>
                            <xsl:choose>
                                <xsl:when test="Amount != ''">
                                    <xsl:value-of select="Amount"/>
                                </xsl:when>
                                <xsl:otherwise>0</xsl:otherwise>
                            </xsl:choose>
                        </Amount>
                        <Quantity>
                            <xsl:choose>
                                <xsl:when test="Quantity != ''">
                                    <xsl:value-of select="Quantity"/>
                                </xsl:when>
                                <xsl:otherwise>0</xsl:otherwise>
                            </xsl:choose>
                        </Quantity>
                    </Fact>
                </xsl:for-each>
            </Facts>
        </DataWarehouse>
    </xsl:template>
</xsl:stylesheet>
```