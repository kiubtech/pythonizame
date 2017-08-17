/**
 * Created by gaspar on 04/05/15.
 */

var pythonizame = {
    blog:function(){



        // $('.post_like').on('click',function(){
        //         var idPost = $(this).data('id');
        //
        //         if(validarLogin()){
        //             doLike(idPost);
        //         }
        //     });
        //
        // $('.post_favorite').on('click',function(){
        //        var idPost = $(this).data('id');
        //         if(validarLogin()){
        //             doFavorite(this,idPost);
        //         }
        //     });
        //
        //
        //
        //
        //
        // function validarLogin(){
        //     if(authenticated!=undefined && authenticated) {
        //         return true;
        //     }else {
        //         alertify.success('Para estas acciones necesitas estar logeado');
        //         return false;
        //     }
        // }
        //
        // function doFavorite(element,idPost){
        //     $.ajax({
        //         url:'/ws/add/favorite/',
        //         dataType:'json',
        //         type:'post',
        //         data:{post:idPost},
        //         success:function(response){
        //             if(!response.is_error){
        //                 if(response.is_favorite){
        //                     $('.favorite'+idPost).addClass('postfavorite');
        //                 }else{
        //                     $('.favorite'+idPost).removeClass('postfavorite');
        //                 }
        //             }
        //             console.log(response);
        //         },
        //         error:function(response){
        //             console.log(response);
        //         }
        //     });
        // }
        //
        //
        // function doLike(idPost){
        //     $.ajax({
        //         url:'/ws/add/like/',
        //         dataType:'json',
        //         type:'post',
        //         data:{post:idPost},
        //         success:function(response){
        //             if(!response.is_error){
        //                 if(response.is_like){
        //                     $('.heart'+idPost).removeClass('fa-heart-o').addClass('fa-heart').addClass('postLike');
        //                 }else{
        //                     $('.heart'+idPost).removeClass('fa-heart').addClass('fa-heart-o').removeClass('postLike');
        //                 }
        //                 $('.num_likes'+idPost).text(response.num_likes);
        //             }
        //             console.log(response);
        //         },
        //         error:function(response){
        //             console.log(response);
        //         }
        //     });
        // }

    },//Blog
    profile:function(){
     var $image = $('#container-pic > img');
     // var $imageCover = $('#container-pic-cover > img');
     //
     //    //aplicamos cropper a los elementos
     //    $imageCover.cropper({
     //        aspectRatio: 16 / 9,
     //        crop: function(data) {
     //            // Output the result data for cropping image.
     //            $('#container-pic-cover').append(data);
     //            var result = $imageCover.cropper('getCroppedCanvas');
     //            var dataUrl = result.toDataURL();
     //        }
     //    });
     //
     //    $image.cropper({
     //          aspectRatio: 10 / 9,
     //          crop: function(data) {
     //            // Output the result data for cropping image.
     //              $('#container-pic').append(data);
     //              var result = $image.cropper('getCroppedCanvas');
     //                var dataUrl = result.toDataURL();
     //          }
     //        });
     //
     //
     //    $('#btnCrop').on('click',function(){
     //            var result = $image.cropper('getCroppedCanvas');
     //            var dataUrl = result.toDataURL();
     //            $('#preview').attr("src",dataUrl);
     //            var formData = new FormData();
     //            formData.append("image_profile",dataUrl);
     //            $('#btnCancelCrop, #btnCrop').attr("disabled","disabled");
     //            $('#btnCrop').text("GUARDANDO...");
     //              $.ajax('/account/ws/change/image_profile/', {
     //                method: "POST",
     //                data: formData,
     //                processData: false,
     //                contentType: false,
     //                success: function (response) {
     //                  $('#imgperfil, #imgProfileNav').attr('src',dataUrl);
     //                  $('#modalProfilepic').modal('hide');
     //                     $('#btnCancelCrop, #btnCrop').removeAttr("disabled")
     //                     $('#btnCrop').text("GUARDAR");
     //                },
     //                error: function (response) {
     //                    $('#btnCancelCrop, #btnCrop').removeAttr("disabled");
     //                    $('#btnCrop').text("GUARDAR");
     //                }
     //              });
     //        });

        // $('#btnCropCover').on('click',function(){
        //         var result = $imageCover.cropper('getCroppedCanvas');
        //         var dataUrl = result.toDataURL();
        //         $('#btnCancelCropCover, #btnCropCover').attr("disabled","disabled");
        //         $('#btnCropCover').text("GUARDANDO...");
        //         var fData = new FormData();
        //         fData.append("image_cover_profile",dataUrl);
        //           $.ajax('/account/ws/change/image_profile/', {
        //             method: "POST",
        //             data: fData,
        //             processData: false,
        //             contentType: false,
        //             success: function (response) {
        //                 location.reload();
        //               $('#modalCoverImage').modal('hide');
        //               $('#btnCancelCropCover, #btnCropCover').removeAttr("disabled");
        //                   $('#btnCropCover').text("GUARDAR");
        //             },
        //             error: function (response) {
        //                alertify.success(response.message.text);
        //                 $('#btnCancelCropCover, #btnCropCover').removeAttr("disabled")
        //                     $('#btnCropCover').text("GUARDAR");
        //             }
        //           });
        //     });

        //cambia la imagen de perfil  de cropper al seleccionar otra con input file
        $('#image_profile').on('change',function(){
            var input = this;
            var fReader = new FileReader();
            console.log('entra');
            fReader.readAsDataURL(input.files[0]);
            fReader.onloadend=function(event){
                var valorMB = event.total/1048576;
                if(valorMB>5){
                    alert('no se pueden cargar imagenes de mas de 5mb');
                    input.value=null;
                }else{
                    $image.cropper('replace', event.target.result);
                }

            };

            fReader.onerror=function(event){
            };
        });

        //cambia la imagen de cover  de cropper al seleccionar otra con input file
        $('#image-cover').on('change',function(){
            var input = this;
            var fReader = new FileReader();
            fReader.readAsDataURL(input.files[0]);
            fReader.onloadend=function(event){
                var valorMB = event.total/1048576;
                if(valorMB>5){
                    alert('no se pueden cargar imagenes de mas de 5mb');
                    input.value=null;
                }else {
                    $imageCover.cropper('replace', event.target.result);
                }
            }

            fReader.onerror=function(event){
            };
        });

},
    register:function(){
        $('#id_username').on('keypress',function(e){
            if(e.keyCode==32){
                e.preventDefault();
            }
        });

        $('#id_username').on('keyup',function(e){
            var username = $(this).val();
            if(e.keyCode!=32){
                validarUserName(this,username);
            }
        });

        $('#id_username').on('validar_init',function(){
             var username = $(this).val();
            if(username!=""){
                validarUserName(this,username);
            }
        });


        $('#id_username').trigger('validar_init');




        function validarUserName(ele,username){
            //debugger;
            $.ajax('/account/ws/validate/username/', {
                method: "POST",
                data: {'username':username},
                success: function (response){
                    var id = ele.id;
                    var $ele = $('.form-group[data-rel='+id+']');
                    if (response.is_available) {
                        $ele.addClass('has-success').removeClass('has-error').next('.message').html('<small style="color:green">'+response.message.text+'</small>');
                        $('#btnRegistro').removeAttr("disabled");
                    } else {
                        $ele.addClass('has-error').removeClass('has-success').next('.message').html('<small style="color:red">'+response.message.text+'</small>');
                        $('#btnRegistro').attr("disabled","disabled");
                    }
                },
                error: function (response) {
                }
            });
        }

        $('#btnRegistro').on('click',function(){
           $(this).val("Registrando..").attr('disabled','disabled');
           $('#frmRegister').submit();
        });
    },
    recoverPassword:function(){
        $('#btnRecuperar').on('click',function(){
            $(this).attr('disabled','disabled').val("Recuperando..");
            $('#frmRecover').submit();
        })
    },
    new_post:function(){

        $('#post_tags').chosen({
            placeholder_text_multiple: "selecciona uno o mas poderes",
            no_results_text: "Oops ningún resultado encontrado!",
        });

        $('.image_new_post').on('change',function(){
            var input = this;
            var fReader = new FileReader();
            fReader.readAsDataURL(input.files[0]);
            fReader.onloadend=function(event){
                var valorMB = event.total/1048576;
                if(valorMB>5){
                    alertify.error('No se pueden cargar imagenes de mas de 5mb');
                    input.value=null;
                }
            };
            fReader.onerror=function(event){
            };
        });
    },
    jobs_mylist:function () {
        $('.delete_job').on('click',function () {
                $('#btnDeleteJob').attr('href',$(this).data('url'));
        });


        $('.revision_job').on('click',function () {
                $('#btnRevJob').attr('href',$(this).data('url'));
        });
    },
    jobs_list:function () {

    }
};

$('[data-toggle="tooltip"]').tooltip();