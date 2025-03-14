Imports System.Data.SqlClient
Imports System.Web
Public Class products
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Public Sub populate()
        Con.Open()
        Dim sql = "select * from ProductTable"
        Dim adapter As SqlDataAdapter
        adapter = New SqlDataAdapter(sql, Con)
        Dim builder As SqlCommandBuilder
        builder = New SqlCommandBuilder(adapter)
        Dim ds As DataSet
        ds = New DataSet
        adapter.Fill(ds)
        ProductDGV.DataSource = ds.Tables(0)
        Con.Close()
    End Sub
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Try
            Con.Open()
            Dim query As String
            query = "insert into ProductTable values ('" & ProductID.Text & "', '" & ProductName.Text & "', '" & Quantity.Text & "', '" & Price.Text & "', '" & Description.Text & "', '" & CategoryName.SelectedValue.ToString() & "')"
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Product Added Succesfully")
            Con.Close()
            populate()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try

    End Sub
    Private Sub FillCategory()
        Con.Open()
        Dim sql = "select * from CategoryTable"
        Dim cmd As New SqlCommand(sql, Con)
        Dim adapter As New SqlDataAdapter(cmd)
        Dim table As New DataTable
        adapter.Fill(table)
        CategoryName.DataSource = table
        CategoryName.DisplayMember = "CategoryName"
        CategoryName.ValueMember = "CategoryName"
        Con.Close()
    End Sub

    Private Sub products_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        populate()
        FillCategory()
    End Sub

    Private Sub Button5_Click(sender As Object, e As EventArgs)
        Application.Exit()
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        If ProductID.Text = "" Then
            MsgBox("Enter the product to be Deleted")
        Else
            Con.Open()
            Dim query As String
            query = "delete from ProductTable where ProductID = " & ProductID.Text & ""
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Product deleted successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        ProductID.Text = ""
        ProductName.Text = ""
        Quantity.Text = ""
        Price.Text = ""
        Description.Text = ""
    End Sub
    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        If ProductID.Text = "" Or ProductName.Text = "" Or Quantity.Text = "" Or Price.Text = "" Or Description.Text = "" Then
            MsgBox("Incomplete Data")
        Else
            Con.Open()
            Dim sql = "update ProductTable set ProductName = '" & ProductName.Text & "',Quantity ='" & Quantity.Text & "',price ='" & Price.Text & "',Description = '" & Description.Text & "',CategoryName ='" & CategoryName.SelectedValue.ToString & "'where ProductID = " & ProductID.Text & ""
            Dim cmd As New SqlCommand(sql, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Product Edited Successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        Dim d As New Dashboard
        d.Show()
        Me.Hide()
    End Sub

    Private Sub Button5_Click_1(sender As Object, e As EventArgs) Handles Button5.Click
        If ProductID.Text = "" Then
            MsgBox("Enter ProductID")
        ElseIf Quantity.Text = "" Then
            MsgBox("Enter Quantity to update")
        Else
            Con.Open()
            Dim sql = "update ProductTable set Quantity ='" & Quantity.Text & "'where ProductID = " & ProductID.Text & ""
            Dim cmd As New SqlCommand(sql, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Product Quantity Updated Successfully")
            Con.Close()
            populate()
        End If
    End Sub
End Class