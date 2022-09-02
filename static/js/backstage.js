function SendAjax(studentNo, studentName, studentSex) {
    $.ajax({
        url: "http://127.0.0.1:5555/getStu",
        method: "POST",
        data: {
            No: studentNo,
            Name: studentName,
            Sex: studentSex
        },
        success: function (data) {
            if (data["code"] == 200) {
                let text = "<tr class=\"stu_tr\">\n" +
                    "                        <th scope=\"row\">" + studentNo + "</th>\n" +
                    "                        <td>" + studentName + "</td>\n" +
                    "                        <td>" + studentSex + "</td>\n" +
                    "                        <td>\n" +
                    "                            <a class=\"btn btn-success btn-sm\">编辑</a>\n" +
                    "                            <a class=\"btn btn-danger btn-sm\">删除</a>\n" +
                    "                        </td>\n" +
                    "                    </tr>"
                $("tr:last").after(text);
                $("#stuNo").val("");
                $("#stuName").val("");
                $("#stuSex").val("");
                alert("添加成功")
            } else {
                alert("已经存在该学号的信息")
            }
        },
        error: function () {
            alert("执行失败了...")
        }
    });
}

$(document).ready(function () {
    $('#bth_get').click(function (event) {
        let studentNo = $("#stuNo").val();
        let studentName = $("#stuName").val();
        let studentSex = $("#stuSex").val();
        if (studentNo.length === 0 || studentName.length === 0 || studentSex.length === 0) {
            alert("学号,密码或者性别为空");
            event.preventDefault();
        } else {
            SendAjax(studentNo, studentName, studentSex)
        }
    })
})

//删除
$(document).ready(function () {
    $(document).on("click", ".stu_tr a:odd", function () {
        let No = $(this).parent().siblings("th").text();
        let Confirm = confirm("是否删除学号为:" + No + "学生信息");
        if (Confirm === true) {

            $.ajax({
                url: "http://127.0.0.1:5555/delStu",
                method: "POST",
                data: {
                    No: No
                },
                success: function (data) {
                    if (data["code"] == 200) {
                        $(this).parent().parent().remove();
                    }
                },
                error: function () {
                    alert("操作失败请稍后重试")
                }
            })
        }
    })
});

//编辑
$(document).ready((function () {
    $(document).on("click", ".stu_tr a:even", function () {
        let no = $(this).parent().siblings("th").text();
        $(this).attr("href", "http://127.0.0.1:5555/modifyStu/" + no)
    })
}))


$(document).ready(function () {
    $(".panel-heading").click(function () {
        $(".panel-body").slideToggle("slow");
    });
});
function modifyStu(no) {
    alert(no)
}