from users.models import Profile


def add_xp(user, amount):
    profile = user.profile
    profile.xp += amount

    # Level scaling system
    while profile.xp >= profile.level * 100:
        profile.xp -= profile.level * 100
        profile.level += 1

    profile.save()