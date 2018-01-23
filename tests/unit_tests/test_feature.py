from unittest import TestCase

from web.models import Feature

class FeaturesTests(TestCase):


    def test_features_priority_adjustment(self):
        """
        Ensure that when creating a new feature that has the same priority as another one it should adjust the priorities

        """

        features = []
        for i in range(10):
            new_feature = Feature("Title {}".format(i+1), None, None, i + 1, None, None)
            new_feature.id = i + 1
            features.append(new_feature)
        
        new_feature = Feature("New Feature", None, None, 5, None, None)
        new_feature.id = 11
        features.append(new_feature)
        new_feature.adjust_features_priority(features)
        self.assertEqual(new_feature.client_priority, 5)
        for i in range(11):
            print(i, features[i].client_priority)
            if i < 4:
                self.assertEqual(features[i].client_priority, i+1)
            elif i == 10:
                self.assertEqual(features[i].client_priority, 5)
            else:
                self.assertEqual(features[i].client_priority, i+2)
        
                
