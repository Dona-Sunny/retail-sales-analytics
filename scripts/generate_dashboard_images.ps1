$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms.DataVisualization
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$cleanedCsv = Join-Path $root "data\cleaned\retail_sales_cleaned.csv"
$imagesDir = Join-Path $root "images"

if (-not (Test-Path $cleanedCsv)) {
    throw "Cleaned dataset not found at $cleanedCsv"
}

New-Item -ItemType Directory -Force -Path $imagesDir | Out-Null
$rows = Import-Csv $cleanedCsv

function New-Chart {
    param(
        [string]$Title,
        [ValidateSet("Column","Bar","Line")] [string]$ChartType,
        [string[]]$Labels,
        [double[]]$Values,
        [string]$YTitle,
        [string]$OutputPath
    )

    $chart = New-Object System.Windows.Forms.DataVisualization.Charting.Chart
    $chart.Width = 1400
    $chart.Height = 850
    $chart.BackColor = [System.Drawing.Color]::FromArgb(248, 249, 252)
    $chart.AntiAliasing = "All"
    $chart.TextAntiAliasingQuality = "High"

    $titleObject = New-Object System.Windows.Forms.DataVisualization.Charting.Title
    $titleObject.Text = $Title
    $titleObject.Font = New-Object System.Drawing.Font("Segoe UI", 24, [System.Drawing.FontStyle]::Bold)
    $titleObject.ForeColor = [System.Drawing.Color]::FromArgb(34, 40, 49)
    $chart.Titles.Add($titleObject) | Out-Null

    $area = New-Object System.Windows.Forms.DataVisualization.Charting.ChartArea "MainArea"
    $area.BackColor = [System.Drawing.Color]::White
    $area.AxisX.MajorGrid.Enabled = $false
    $area.AxisY.MajorGrid.LineColor = [System.Drawing.Color]::FromArgb(230, 233, 240)
    $area.AxisX.LabelStyle.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $area.AxisY.LabelStyle.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $area.AxisY.Title = $YTitle
    $area.AxisY.TitleFont = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
    $area.AxisY.LabelStyle.Format = "N0"
    $chart.ChartAreas.Add($area) | Out-Null

    $legend = New-Object System.Windows.Forms.DataVisualization.Charting.Legend
    $legend.Enabled = $false
    $chart.Legends.Add($legend) | Out-Null

    $series = New-Object System.Windows.Forms.DataVisualization.Charting.Series "Series"
    $series.ChartType = [System.Windows.Forms.DataVisualization.Charting.SeriesChartType]::$ChartType
    $series.Color = [System.Drawing.Color]::FromArgb(27, 94, 154)
    $series.BorderWidth = 3
    $series.IsValueShownAsLabel = $true
    $series.LabelFormat = "N0"
    $series.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)

    for ($i = 0; $i -lt $Labels.Length; $i++) {
        $pointIndex = $series.Points.AddXY($Labels[$i], $Values[$i])
        $series.Points[$pointIndex].Color = [System.Drawing.Color]::FromArgb(27 + (($i * 12) % 100), 94 + (($i * 7) % 60), 154 + (($i * 3) % 50))
    }

    if ($ChartType -eq "Line") {
        $series.Color = [System.Drawing.Color]::FromArgb(12, 115, 80)
        $series.MarkerStyle = [System.Windows.Forms.DataVisualization.Charting.MarkerStyle]::Circle
        $series.MarkerSize = 8
        $series.IsValueShownAsLabel = $false
    }

    $chart.Series.Add($series) | Out-Null
    $chart.SaveImage($OutputPath, "Png")
    $chart.Dispose()
}

$monthly = $rows |
    Group-Object { ([datetime]$_.Order_Date).ToString("yyyy-MM") } |
    ForEach-Object {
        [pscustomobject]@{
            Month = $_.Name
            NetSales = [math]::Round((($_.Group | Measure-Object -Property Net_Sales -Sum).Sum), 2)
        }
    } |
    Sort-Object Month

$category = $rows |
    Group-Object Category |
    ForEach-Object {
        [pscustomobject]@{
            Category = $_.Name
            NetSales = [math]::Round((($_.Group | Measure-Object -Property Net_Sales -Sum).Sum), 2)
        }
    } |
    Sort-Object NetSales -Descending |
    Select-Object -First 6

$customer = $rows |
    Group-Object Customer_Name |
    ForEach-Object {
        [pscustomobject]@{
            Customer = $_.Name
            NetSales = [math]::Round((($_.Group | Measure-Object -Property Net_Sales -Sum).Sum), 2)
        }
    } |
    Sort-Object NetSales -Descending |
    Select-Object -First 8

New-Chart `
    -Title "Dashboard Overview: Monthly Net Sales" `
    -ChartType "Line" `
    -Labels ($monthly.Month) `
    -Values ($monthly.NetSales) `
    -YTitle "Net Sales" `
    -OutputPath (Join-Path $imagesDir "dashboard_overview.png")

New-Chart `
    -Title "Product Analysis: Revenue by Category" `
    -ChartType "Column" `
    -Labels ($category.Category) `
    -Values ($category.NetSales) `
    -YTitle "Revenue" `
    -OutputPath (Join-Path $imagesDir "product_analysis.png")

New-Chart `
    -Title "Customer Analysis: Top Customers by Revenue" `
    -ChartType "Bar" `
    -Labels ($customer.Customer) `
    -Values ($customer.NetSales) `
    -YTitle "Revenue" `
    -OutputPath (Join-Path $imagesDir "customer_analysis.png")
