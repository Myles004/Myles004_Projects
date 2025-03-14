Imports System.Data.SqlClient
Public Class Admin
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Public Sub populate()
        Con.Open()
        Dim sql = "select * from AdminTable"
        Dim adapter As SqlDataAdapter
        adapter = New SqlDataAdapter(sql, Con)
        Dim builder As SqlCommandBuilder
        builder = New SqlCommandBuilder(adapter)
        Dim ds As DataSet
        ds = New DataSet
        adapter.Fill(ds)
        AdminDGV.DataSource = ds.Tables(0)
        Con.Close()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Try
            Con.Open()
            Dim query As String
            query = "insert into AdminTable values ('" & AdminID.Text & "', '" & AdminName.Text & "', '" & AdminPassword.Text & "', '" & AdminPhone.Text & "')"
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Admin Added Succesfully")
            Con.Close()
            populate()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try

    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        AdminID.Text = ""
        AdminName.Text = ""
        AdminPassword.Text = ""
        AdminPhone.Text = ""
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        If AdminID.Text = "" Or AdminName.Text = "" Or AdminPassword.Text = "" Or AdminPhone.Text = "" Then
            MsgBox("Incomplete Data")
        Else
            Con.Open()
            Dim sql = "update AdminTable Set AdminName = '" & AdminName.Text & "',AdminPassword ='" & AdminPassword.Text & "',AdminPhone ='" & AdminPhone.Text & "'where AdminID = " & AdminID.Text & ""
            Dim cmd As New SqlCommand(sql, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Admin Edited Successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        If AdminID.Text = "" Then
            MsgBox("Enter the Admin to be Deleted")
        Else
            Con.Open()
            Dim query As String
            query = "delete from AdminTable where AdminID = " & AdminID.Text & ""
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            cmd.ExecuteNonQuery()
            MsgBox("Admin deleted successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub users_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        populate()
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        Dim d As New Dashboard
        d.Show()
        Me.Hide()
    End Sub

    Private Sub Button7_Click(sender As Object, e As EventArgs) Handles Button7.Click
        Dim u As New users
        u.Show()
        Me.Hide()
    End Sub
End Class