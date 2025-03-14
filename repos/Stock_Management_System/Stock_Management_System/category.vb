Imports System.Data.SqlClient
Public Class category
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Public Sub populate()
        Con.Open()
        Dim sql = "select * from CategoryTable"
        Dim adapter As SqlDataAdapter
        adapter = New SqlDataAdapter(sql, Con)
        Dim builder As SqlCommandBuilder
        builder = New SqlCommandBuilder(adapter)
        Dim ds As DataSet
        ds = New DataSet
        adapter.Fill(ds)
        CategoryDGV.DataSource = ds.Tables(0)
        Con.Close()
    End Sub
    Private Sub Button5_Click(sender As Object, e As EventArgs) 
        Application.Exit()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Try
            Con.Open()
            Dim query As String
            query = "insert into CategoryTable values ('" & CategoryID.Text & "', '" & Categoryname.Text & "')"
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Category Added Succesfully")
            Con.Close()
            populate()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try
    End Sub

    Private Sub category_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        populate()
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        CategoryID.Text = ""
        Categoryname.Text = ""
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        If CategoryID.Text = "" Then
            MsgBox("Enter the Category to be Deleted")
        Else
            Con.Open()
            Dim query As String
            query = "delete from CategoryTable where CategoryID = " & CategoryID.Text & ""
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Category deleted successfully")
            Con.Close()
            populate()
            CategoryID.Text = ""
            Categoryname.Text = ""
        End If
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        If CategoryID.Text = "" Or Categoryname.Text = "" Then
            MsgBox("Incomplete Data")
        Else
            Con.Open()
            Dim sql = "update CategoryTable set CategoryName = '" & Categoryname.Text & "' where CategoryID = " & CategoryID.Text & ""
            Dim cmd As New SqlCommand(sql, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Category Edited Successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        Dim d As New Dashboard
        d.Show()
        Me.Hide()
    End Sub
End Class