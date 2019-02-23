/**
 * Created by Negin on 2/2/2017.
 */

$(document).ready(function() {
    $(function () {
        $('#address-button').click(function () {
            $('#address-field').toggle("slow");
        });
        $( "#close-icon-show" )
            .on("mouseenter", function() {
                $("#close-icon").show("slow");
                $("#close-icon").click(function () {
                //    TODO delete the address field
                })
            })
            .on("mouseleave", function() {
                $("#close-icon").hide("slow");
            });


        $('#submit-btn').click(function () {
            $('form').form('validate form');
            $('form').form('is valid', function () {
                $('form').form('submit');
            });

        });

        $('form')
            .form({
                inline : true,
                on: 'change',
                fields: {
                    نام: {
                        identifier  : 'name',
                        rules: [
                            {
                                type   : 'empty',
                                prompt : 'لطفا نام خود را وارد کنید'
                            }
                        ]
                    },
                    familyName: {
                        identifier  : 'familyName',
                        rules: [
                            {
                                type   : 'empty',
                                prompt : 'لطفا نام خانوادگی خود را وارد کنید'
                            }
                        ]
                    },
                    email: {
                        identifier  : 'email',
                        rules: [
                            {
                                type   : 'empty',
                                prompt : 'لطفا پست الکترونیکی خود را وارد کنید'
                            },
                            {
                                type   :  'email',
                                prompt :  'لطفا پست الکترونیکی را درست وارد کنید'
                            }
                        ]
                    },
                    passwordCurrent: {
                        identifier  : 'passwordCurrent',
                        rules: [
                            {
                                type   :  'minLength[6]',
                                prompt :  'رمز عبور باید بیشتر از 6 باشد'
                            }
                        ]
                    },
                    passwordNew: {
                        identifier  : 'passwordNew',
                        rules: [
                            {
                                type   : 'empty',
                                prompt : 'رمز عبور جدید خالی است'
                            },
                            {
                                type   :  'minLength[6]',
                                prompt :  'رمز عبور جدید باید بیشتر از 6 باشد'
                            },
                            {
                                type   :  'minLength[6]',
                                prompt :  'رمز عبور جدید باید بیشتر از {rulevalue} باشد'
                            }
                        ]
                    },
                    name: {
                        identifier  : 'passwordNewReply',
                        rules: [
                            {
                                type   : 'match[passwordNew]',
                                prompt : 'رمز عبور جدید با تکرار آن هم‌خوانی ندارد'
                            },
                            {
                                type   : 'empty',
                                prompt : 'تکرار رمز عبور جدید خالی است'
                            }
                        ]
                    }
                }
            })
        ;
        $('form').form(validationRules, { onSuccess: submitForm });
    });

});
