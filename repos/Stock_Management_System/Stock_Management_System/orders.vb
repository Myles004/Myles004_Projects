﻿Imports System.Data.SqlClient
Imports Microsoft.VisualBasic.ApplicationServices
Public Class orders
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Private Sub FillProduct()
        Con.Open()
        Dim sql = "select * from ProductTable"
        Dim cmd As New SqlCommand(sql, Con)
        Dim adapter As New SqlDataAdapter(cmd)
        Dim table As New DataTable
        adapter.Fill(table)
        ProductIDCB.DataSource = table
        ProductIDCB.DisplayMember = "ProductID"
        ProductIDCB.ValueMember = "ProductID"
        Con.Close()
    End Sub
    Private Sub FillCustomers()
        Con.Open()
        Dim sql = "select * from CustomerTable"
        Dim cmd As New SqlCommand(sql, Con)
        Dim adapter As New SqlDataAdapter(cmd)
        Dim table As New DataTable
        adapter.Fill(table)
        CustomerIDCB.DataSource = table
        CustomerIDCB.DisplayMember = "CustomerID"
        CustomerIDCB.ValueMember = "CustomerID"
        Con.Close()
    End Sub
    Private Sub FetchName()
        Con.Open()
        Dim query = "Select * from CustomerTable where CustomerID =" & CustomerIDCB.SelectedValue.ToString() & ""
        Dim cmd As New SqlCommand(query, Con)
        Dim table As New DataTable
        Dim reader As SqlDataReader
        reader = cmd.ExecuteReader()
        While reader.Read
            CustomerNameTB.Text = reader(1).ToString()
        End While
        Con.Close()


    End Sub
    Dim ProductName As String
    Dim price As Integer
    Dim AvailQuantity As Integer
    Private Sub Fetchdata()
        Con.Open()
        Dim query = "select * from ProductTable where ProductID =" & ProductIDCB.SelectedValue.ToString() & ""
        Dim cmd As New SqlCommand(query, Con)
        Dim table As New DataTable
        Dim reader As SqlDataReader
        reader = cmd.ExecuteReader()
        While reader.Read
            ProductName = reader(1).ToString()
            price = Convert.ToUInt32(reader(3).ToString())
            AvailQuantity = Convert.ToUInt32(reader(2).ToString())
            ProductNameTB.Text = ProductName
        End While
        Con.Close()
    End Sub
    Private Sub Quantity()
        Try
            Con.Open()
            Dim query As String
            query = "insert into QuantityTable values ('" & ProductIDCB.SelectedValue.ToString & "', '" & QuantityTB.Text & "')"
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            Con.Close()
            populate()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try
    End Sub


    Private Sub orders_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        FillProduct()
        FillCustomers()
        populate()
        TotalAmount()

    End Sub
    Private Sub ProductNameCB_SelectionChangeCommitted(sender As Object, e As EventArgs) Handles ProductIDCB.SelectionChangeCommitted
        Fetchdata()
    End Sub
    Dim Grtot = 0, i = 0, Total = 0
    Public Sub populate()
        Con.Open()
        Dim sql = "select * from OrderTable"
        Dim adapter As SqlDataAdapter
        adapter = New SqlDataAdapter(sql, Con)
        Dim builder As SqlCommandBuilder
        builder = New SqlCommandBuilder(adapter)
        Dim ds As DataSet
        ds = New DataSet
        adapter.Fill(ds)
        OrderDGV.DataSource = ds.Tables(0)
        Con.Close()
    End Sub
    Public Sub TotalAmount()
        Dim query = "select sum(TotalAmount)from OrderTable"
        Dim cmd As SqlCommand
        cmd = New SqlCommand(query, Con)
        Try
            Con.Open()
            Dim result As Object = cmd.ExecuteScalar()
            Totalorderslabel.Text = Convert.ToInt64(result)
            Con.Close()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try
    End Sub
    Private Sub PrintDocument1_PrintPage(sender As Object, e As Printing.PrintPageEventArgs) Handles PrintDocument1.PrintPage
        e.Graphics.DrawString("ANFIELD DRAPERS WHOLESALE ", New Font("Tahoma", 18), Brushes.Blue, 220, 40)
        e.Graphics.DrawString("YOUR ORDER", New Font("Tahoma", 18), Brushes.Blue, 350, 70)
        e.Graphics.DrawString("******************************************************************************************", New Font("Tahoma", 18), Brushes.Red, 0, 10)
        e.Graphics.DrawString("THANK YOU FOR SHOPPING WITH US", New Font("Tahoma", 18), Brushes.Black, 250, 1050)
        e.Graphics.DrawString("******************************************************************************************", New Font("Tahoma", 18), Brushes.Red, 0, 1080)
        e.Graphics.DrawString("TOTAL AMOUNT:Ksh " & Amountlabel.Text & "", New Font("Tahoma", 16), Brushes.Blue, 350, 1020)

        Dim bm As New Bitmap(Me.BillDGV.Width, Me.BillDGV.Height)
        BillDGV.DrawToBitmap(bm, New Rectangle(0, 0, Me.BillDGV.Width, Me.BillDGV.Height))
        e.Graphics.DrawImage(bm, 110, 100)
        InsertOrder()
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        PrintPreviewDialog1.Show()

    End Sub
    Private Sub InsertOrder()
        If CustomerNameTB.Text = "" Then
            MsgBox("Select Customer Name")
        Else
            Try
                Con.Open()
                Dim query As String
                query = "insert into OrderTable values ('" & OrderID.Text & "', '" & CustomerIDCB.SelectedValue.ToString() & "', '" & CustomerNameTB.Text & "'," & Amountlabel.Text & ")"
        Dim cmd As SqlCommand
        cmd = New SqlCommand(query, Con)
        cmd.ExecuteNonQuery()
        MsgBox("Order Added Succesfully")
        Con.Close()
        populate()
        Catch ex As Exception
        MsgBox(ex.Message)
        End Try
        End If
    End Sub
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If QuantityTB.Text = "" Then
            MsgBox("Enter The Product Quantity")
        Else
            Dim rnum As Integer = BillDGV.Rows.Add()
            i = i + 1
            Total = price * Convert.ToInt32(QuantityTB.Text)
            BillDGV.Rows.Item(rnum).Cells("Column1").Value = i
            BillDGV.Rows.Item(rnum).Cells("Column2").Value = ProductNameTB.Text
            BillDGV.Rows.Item(rnum).Cells("Column3").Value = price
            BillDGV.Rows.Item(rnum).Cells("Column4").Value = QuantityTB.Text
            BillDGV.Rows.Item(rnum).Cells("Column5").Value = Total
            Grtot = Grtot + Total
            Amountlabel.Text = Grtot
        End If
    End Sub

    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
        TotalAmount()
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        If OrderID.Text = "" Then
            MsgBox("Please Enter OrderID")
        Else
            Con.Open()
            Dim query As String
            query = "delete from OrderTable where OrderID = " & OrderID.Text & ""
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Order removed successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        OrderID.Text = ""
        ProductNameTB.Text = ""
        CustomerNameTB.Text = ""
        QuantityTB.Text = ""
    End Sub

    Private Sub CustomerIDCB_SelectionChangeCommitted(sender As Object, e As EventArgs) Handles CustomerIDCB.SelectionChangeCommitted
        FetchName()
    End Sub


    Private Sub Button2_Click_1(sender As Object, e As EventArgs) Handles Button2.Click
        Dim d As New Dashboard2
        d.Show()
        Me.Hide()
    End Sub
End Class

