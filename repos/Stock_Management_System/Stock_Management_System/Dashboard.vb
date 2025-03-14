Imports System.Data.SqlClient
Public Class Dashboard
    Dim Con As New SqlConnection("Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\dom\Documents\StockvbDB.mdf;Integrated Security=True;Connect Timeout=30")
    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
        Application.Exit()
    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        Dim u As New users
        u.Show()
        Me.Hide()
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim c As New Customers
        c.Show()
        Me.Hide()
    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        Dim p As New products
        p.Show()
        Me.Hide()
    End Sub

    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        Dim s As New category
        s.Show()
        Me.Hide()
    End Sub

    Private Sub LinkLabel1_LinkClicked(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles LinkLabel1.LinkClicked
        Dim x As New login
        x.Show()
        Me.Hide()
    End Sub

    Private Sub Button6_Click(sender As Object, e As EventArgs)
        Dim o As New orders
        o.Show()
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

    Private Sub Button6_Click_1(sender As Object, e As EventArgs) Handles Button6.Click
        Dim o As New orders2
        o.Show()
        Me.Hide()
    End Sub

End Class