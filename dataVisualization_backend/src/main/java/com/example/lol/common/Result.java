package com.example.lol.common;

import lombok.Data;

@Data
public class Result {
    private int code;// 成功为200 失败为400
    private String msg;// suc / fail
    private int total;// 记录数
    private Object data;// 数据

    private static Result result(int code, String msg, int total, Object data) {
        Result res = new Result();
        res.setCode(code);
        res.setMsg(msg);
        res.setTotal(total);
        res.setData(data);
        return res;
    }

    public static Result fail() {
        return result(400, "失败", 0, null);
    }

    public static Result fail(String msg) {
        return result(400, msg, 0, null);
    }

    public static Result suc() {
        return result(200, "成功", 0, null);
    }

    public static Result suc(Object data) {
        return result(200, "成功", 0, data);
    }

    public static Result suc(Object data, int total) {
        return result(200, "成功", total, data);
    }

}
