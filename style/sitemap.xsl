<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
		xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html" doctype-system="about:legacy-compat" encoding="UTF-8" indent="yes" />
	<xsl:template match="/">
		<html>
			<head>
				<title>Jakub Tesárek | Sitemap</title>
				<link href="/style/sitemap.css" type="text/css" rel="stylesheet" />
			</head>
			<body>
				<h1>Sitemap of tesarek.me</h1>
				<xsl:call-template name="sitemapTable" />
			</body>
		</html>
	</xsl:template>

	<xsl:template name="sitemapTable">
		<table>
			<thead>
				<tr>
					<th>URL</th>
					<th>Last modification</th>
					<th>Change frequency</th>
					<th>Priority</th>
				</tr>
			</thead>
			<tbody>
				<xsl:apply-templates select="sitemap:urlset/sitemap:url">
					<xsl:sort select="sitemap:priority" order="descending" />
				</xsl:apply-templates>
			</tbody>
		</table>
	</xsl:template>

	<xsl:template match="sitemap:url">
		<tr>
			<td>
				<xsl:variable name="sitemapURL">
					<xsl:value-of select="sitemap:loc" />
				</xsl:variable>
				<a href="{$sitemapURL}" ref="nofollow"><xsl:value-of select="$sitemapURL" /></a>
			</td>
			<td>
				<xsl:variable name="sitemapLastmod">
					<xsl:value-of select="sitemap:lastmod" />
				</xsl:variable>
				<time datetime="{$sitemapLastmod}"><xsl:value-of select="$sitemapLastmod" /></time>
			</td>
			<td>
				<xsl:value-of select="sitemap:changefreq" />
			</td>
			<td>
				<xsl:choose>
					<xsl:when test="sitemap:priority">
						<xsl:value-of select="sitemap:priority"/>
					</xsl:when>
					<xsl:otherwise>0.5</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>
</xsl:stylesheet>