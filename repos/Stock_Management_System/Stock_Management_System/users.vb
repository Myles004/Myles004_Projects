Imports System.Data.SqlClient
Public Class users
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Public Sub populate()
        Con.Open()
        Dim sql = "select * from UserTable"
        Dim adapter As SqlDataAdapter
        adapter = New SqlDataAdapter(sql, Con)
        Dim builder As SqlCommandBuilder
        builder = New SqlCommandBuilder(adapter)
        Dim ds As DataSet
        ds = New DataSet
        adapter.Fill(ds)
        UserDGV.DataSource = ds.Tables(0)
        Con.Close()
    End Sub
    Private Sub Button5_Click(sender As Object, e As EventArgs)
        Application.Exit()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If UserID.Text = "" Or UserName.Text = "" Or UserPassword.Text = "" Or UserPhone.Text = "" Then
            MsgBox("Incomplete Data")
        Else
            Try
                Con.Open()
                Dim query As String
                query = "insert into UserTable values ('" & UserID.Text & "', '" & UserName.Text & "', '" & UserPassword.Text & "', '" & UserPhone.Text & "')"
                Dim cmd As SqlCommand
                cmd = New SqlCommand(query, Con)
                cmd.ExecuteNonQuery()
                MsgBox("User Added Succesfully")
                Con.Close()
                populate()
            Catch ex As Exception
                MsgBox(ex.Message)
            End Try
        End If
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        UserID.Text = ""
        UserName.Text = ""
        UserPassword.Text = ""
        UserPhone.Text = ""
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        If UserID.Text = "" Or UserName.Text = "" Or UserPassword.Text = "" Or UserPhone.Text = "" Then
            MsgBox("Incomplete Data")
        Else
            Con.Open()
            Dim sql = "update UserTable Set UserName = '" & UserName.Text & "',UserPassword ='" & UserPassword.Text & "',UserPhone ='" & UserPhone.Text & "' where UserID = " & UserID.Text & ""
            Dim cmd As New SqlCommand(sql, Con)
            cmd.ExecuteNonQuery()
            MsgBox("User Edited Successfully")
            Con.Close()
            populate()
        End If
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        If UserDGV.SelectedRows.Count > 0 Then
            Dim dt As DataTable = CType(UserDGV.DataSource, DataTable)
            For Each row As DataGridViewRow In UserDGV.SelectedRows
                dt.Rows.Remove(CType(row.DataBoundItem, DataRowView).Row)
            Next
            UserDGV.DataSource = dt
        Else
            MsgBox("please select a row to delete.")
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

    Private Sub Button5_Click_1(sender As Object, e As EventArgs) Handles Button5.Click
        Dim a As New Admin
        a.Show()
        Me.Hide()
    End Sub

   End Class