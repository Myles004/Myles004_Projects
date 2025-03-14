Imports System.Data.SqlClient
Public Class login2
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim r As New role
        r.Show()
        Me.Hide()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If Usernamelg.Text = "" Then
            MsgBox("Enter username")
        ElseIf Password.Text = "" Then
            MsgBox("Enter password")
        Else
            Con.Open()
            Dim query = "select * from UserTable where UserName = '" & Usernamelg.Text & "'and UserPassword ='" & Password.Text & "'"
            Dim cmd As SqlCommand
            cmd = New SqlCommand(query, Con)
            Dim da As SqlDataAdapter = New SqlDataAdapter(cmd)
            Dim ds As DataSet = New DataSet()
            da.Fill(ds)
            Dim a As Integer
            a = ds.Tables(0).Rows.Count
            If a = 0 Then
                MsgBox("Wrong Username and Password")
            Else
                Dim d As New Dashboard2
                d.Show()
                Me.Hide()
            End If
            Con.Close()
        End If
    End Sub

    Private Sub login2_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub
End Class