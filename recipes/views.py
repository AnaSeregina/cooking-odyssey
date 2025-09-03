import random
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm

def home(request):
    recipes = Recipe.objects.order_by("-created_at")
    return render(request, "home.html", {"recipes": recipes})

# def recipe_detail(request, slug):
#     r = get_object_or_404(Recipe, slug=slug)
#     return render(request, "recipe_detail.html", {"r": r})

def nutrition_table(request):
    recipes = Recipe.objects.order_by("title")
    return render(request, "nutrition.html", {"recipes": recipes})

def about(request):
    return render(request, "about.html")

def contacts(request):
    return render(request, "contacts.html")


SUPPORT_MESSAGES = [
    {
        "emoji_start": "<span class='star-accent'>✦</span>",
        "text": "Enjoyed this cosmic dish?",
        "link_text": "Fuel the Odyssey",
        "emoji_end": "<span class='star-accent'>✦</span>",
    },
    {
        "emoji_start": "<span class='star-accent'>✦</span>",
        "text": "If this recipe made you smile,",
        "link_text": "show a little love",
        "emoji_end": "<span class='star-accent'>✦</span>",
    },
    {
        "emoji_start": "<span class='star-accent'>✦</span>",
        "text": "Hungry for more adventures?",
        "link_text": "Support Cooking Odyssey",
        "emoji_end": "<span class='star-accent'>✦</span>",
    },
]

def recipe_detail(request, slug):
    r = get_object_or_404(Recipe, slug=slug)
    support_message = random.choice(SUPPORT_MESSAGES)
    return render(request, "recipe_detail.html", {"r": r, "support_message": support_message})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            fun = form.cleaned_data.get("fun_question", "")

            subject = f"[Cooking Odyssey] New contact form message from {name}"
            lines = [
                f"Name: {name}",
                f"Email: {email}",
                f"Fun answer: {fun or '(none)'}",
                "",
                "Message:",
                message,
            ]
            body = "\n".join(lines)

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=getattr(settings, "CONTACT_RECIPIENTS", [settings.DEFAULT_FROM_EMAIL]),
                fail_silently=False,
            )

            messages.success(request, "<span class='star-accent'>✦</span> Thank you! Your message has been sent <span class='star-accent'>✦</span>")
            return redirect("contact")  # show empty form again with success banner
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})