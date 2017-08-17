import json


class Object:

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class LazyUserProfileData(Object):

    def __init__(self, object_data=None):
        if object_data:
            if 'website' in object_data:
                self.website = object_data['website']
            if 'about_me' in object_data:
                self.about_me = object_data['about_me']
            if 'country_code' in object_data:
                self.country_code = object_data['country_code']
            if 'twitter' in object_data:
                self.twitter = object_data['twitter']
            if 'facebook' in object_data:
                self.facebook = object_data['facebook']
            if 'github' in object_data:
                self.github = object_data['github']
            if 'gender' in object_data:
                self.gender = object_data['gender']
        else:
            self.website = ""
            self.about_me = ""
            self.country_code = ""
            self.gender = ""
            self.twitter = ""
            self.facebook = ""
            self.github = ""
