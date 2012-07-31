from tree import iter_tree, enumerate_paths, find_by_path, from_path_list, path_from_string
from nose.tools import assert_equal, raises
from exceptions import ValueError

TECHNOLOGIES = { 
    'name': 'Technology',
    'children': [
        {'name': 'Programming',
        'children': [ {'name': 'Python'}, {'name': 'Ruby'}]},
        {'name': 'Enterprise',
         'children': [ {'name': 'Mac'}, {'name': 'Mobile'}]}]
    }

class TestTree:

    def test_enumerate_paths(self):
        assert_equal([
            (['Technology'], 'Technology'),
            (['Technology', 'Programming'], 'Programming'),
            (['Technology', 'Programming', 'Python'], 'Python'),
            (['Technology', 'Programming', 'Ruby'], 'Ruby'),
            (['Technology', 'Enterprise'], 'Enterprise'),
            (['Technology', 'Enterprise', 'Mac'], 'Mac'),
            (['Technology', 'Enterprise', 'Mobile'], 'Mobile')],
            list((path, node['name']) for path, node in enumerate_paths(TECHNOLOGIES)))


    def test_find_by_path(self):
       assert_equal({'name': 'Python'},
            find_by_path(TECHNOLOGIES, ['Technology', 'Programming', 'Python']))

    def test_find_by_path_when_not_found(self):
       assert_equal(None,
            find_by_path(TECHNOLOGIES, ['Technology', 'does_not_exist']))

    def test_iter_tree(self):
        assert_equal([{'children': [{'children': [{'name': 'Python'}, {'name': 'Ruby'}],
                       'name': 'Programming'},
                      {'children': [{'name': 'Mac'}, {'name': 'Mobile'}],
                       'name': 'Enterprise'}],
                     'name': 'Technology'},
                {'children': [{'name': 'Python'}, {'name': 'Ruby'}], 'name': 'Programming'},
                {'name': 'Python'},
                {'name': 'Ruby'},
                {'children': [{'name': 'Mac'}, {'name': 'Mobile'}], 'name': 'Enterprise'},
                {'name': 'Mac'},
                {'name': 'Mobile'}],
        list(iter_tree(TECHNOLOGIES)))

    def test_generator_expression(self):
        assert_equal(['Technology', 'Programming', 'Python', 'Ruby',
                    'Enterprise', 'Mac', 'Mobile'],
            list(e['name'] for e in iter_tree(TECHNOLOGIES)))

        assert_equal(['Python', 'Ruby', 'Mac', 'Mobile'],
            list(e['name'] for e in iter_tree(TECHNOLOGIES) if is_leaf(e)))

    def test_update_with_side_effect(self):
        technologies = {
            'name': 'Technology',
            'children': [
            {
                'name': 'Programming',
                'children': [
                {'name': 'Python'},
                {'name': 'Ruby'}
                ]
            }]}

        python = (e for e in iter_tree(technologies) if e['name'] == 'Python').next()
        python.update(tag='cool')

        assert_equal({
            'name': 'Technology',
            'children': [
            {
                'name': 'Programming',
                'children': [
                {'name': 'Python', 'tag': 'cool'},
                {'name': 'Ruby'}
                ] }]},
        technologies)

    def test_path_from_string(self):
        assert_equal(['a', 'b', 'c'], path_from_string('/a/b/c'))
    
    @raises(ValueError)
    def test_path_from_string(self):
        path_from_string('a/b/c')

    def test_from_path_list(self):
        assert_equal({}, from_path_list([]))
        assert_equal({'name': 'a'}, from_path_list(['/a']))
        assert_equal({'name': 'a', 'children': [{'name': 'b'}]}, from_path_list(['/a/b']))
        assert_equal({'name': 'a', 'children': [{'name': 'b'}]}, from_path_list(['/a', '/a/b']))
        assert_equal({'name': 'a', 'children': [{'name': 'b'}]}, from_path_list(['/a/b', '/a']))

        assert_equal(
            {'name': 'a', 
             'children': [{'name': 'b'},
                          {'name': 'c', 
                                'children': [{'name': 'd'}]}]}, 
            from_path_list(['/a/b', '/a/c/d']))

        assert_equal(
            {'name': 'a', 
             'children': [{'name': 'c', 
                                'children': [{'name': 'd'}]},
                          {'name': 'b'}]}, 
            from_path_list(['/a/c/d', '/a/b']))

def is_leaf(e):
    return 'children' not in e
