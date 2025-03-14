Imports System.Data.SqlClient
Public Class Dashboard2
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
        Application.Exit()
    End Sub
    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim c As New customers2
        c.Show()
        Me.Hide()
    End Sub
    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
        Dim o As New orders
        o.Show()
        Me.Hide()
    End Sub
    Private Sub LinkLabel1_LinkClicked(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles LinkLabel1.LinkClicked
        Dim x As New login
        x.Show()
        Me.Hide()
    End Sub
    Private Sub TotalAmount()
        Dim query = "select sum(TotalAmount)from OrderTable"
        Dim cmd As SqlCommand
        cmd = New SqlCommand(query, Con)
        Try
            Con.Open()
            Dim result As Object = cmd.ExecuteScalar()
            TotalOrderslabel.Text = Convert.ToInt64(result)
            Con.Close()
        Catch ex As Exception
            MsgBox(ex.Message)
        End Try

    End Sub
    Private Sub Dashboard_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Dim query = "select count(*) from CustomerTable"
        Dim query1 = "select count(*) from OrderTable"
        Dim cmd As SqlCommand
        Dim cmd1 As SqlCommand
        Con.Open()
        cmd = New SqlCommand(query, Con)
        Dim count As Int16 = Convert.ToInt16(cmd.ExecuteScalar())
        Customercountlabel.Text = count.ToString()
        cmd1 = New SqlCommand(query1, Con)
        Dim count1 As Int16 = Convert.ToInt16(cmd1.ExecuteScalar())
        Orderscountlabel.Text = count1.ToString()
        Con.Close()
        TotalAmount()
    End Sub
End Class