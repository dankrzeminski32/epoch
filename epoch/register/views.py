from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserConfigForm, EmailSettingsForm, ExportSettingsForm, TextSettingsForm
from .models import UserConfig


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user_cfg = UserConfig(user=new_user)
            new_user_cfg.save()
            login(request, new_user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})


def edit_user_settings(request):
    current_user = request.user
    if request.method == "POST":
        user_config_form = UserConfigForm(
            request.POST, instance=current_user.userconfig)
        email_settings_form = EmailSettingsForm(request.POST,
                                                instance=current_user.userconfig.email_settings)
        text_settings_form = TextSettingsForm(request.POST,
                                              instance=current_user.userconfig.text_settings)
        export_settings_form = ExportSettingsForm(request.POST,
                                                  instance=current_user.userconfig.export_settings)
        setting_forms = [user_config_form, email_settings_form,
                         text_settings_form, export_settings_form]
        if all([form.is_valid() for form in setting_forms]):
            for form in setting_forms:
                print(form)
                form.save()
            messages.success(request, "Successfully updated your profile.")
            return render(request, "registration/user-settings.html", {"user_config_form": user_config_form, "email_settings_form": email_settings_form, "text_settings_form": text_settings_form, "export_settings_form": export_settings_form})
        else:
            return render(request, "registration/user-settings.html", {"user_config_form": user_config_form, "email_settings_form": email_settings_form, "text_settings_form": text_settings_form, "export_settings_form": export_settings_form, "all_forms": setting_forms})
    else:
        user_config_form = UserConfigForm(instance=current_user.userconfig)
        email_settings_form = EmailSettingsForm(
            instance=current_user.userconfig.email_settings)
        print(current_user.userconfig.text_settings.phone_number)
        text_settings_form = TextSettingsForm(
            instance=current_user.userconfig.text_settings)
        export_settings_form = ExportSettingsForm(
            instance=current_user.userconfig.export_settings)
        return render(request, "registration/user-settings.html", {"user_config_form": user_config_form, "email_settings_form": email_settings_form, "text_settings_form": text_settings_form, "export_settings_form": export_settings_form})
