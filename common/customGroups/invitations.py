def process_invitation(invitation, user):
    invitation.group.members.add(
        user, through_defaults={"role": invitation.role}
    )
    invitation.is_accepted = True
    invitation.accepted_by = user
    invitation.save()


def get_invitation_unique_from_request(request):
    return request.GET.get("invitation_unique") or request.session.get(
        "invitation_unique"
    )


def clear_invite_from_session(request):
    if "invitation_unique" in request.session:
        del request.session["invitation_unique"]
