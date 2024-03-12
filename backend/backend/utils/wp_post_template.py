import requests

class post_val:
    def __init__(self, post_type, post_id, user_id, property_type, property_name, presentation_condition, price,
                 maximum_price, move_in_date, image, address, map, access, parking, floor_plan, transaction_form,
                 exclusive_area, building_area, land_area, balcony_area, site_area, total_sales, price_range,
                 direction_access, road_conditions, land_rights, building_coverage, floor_area, use_area, landmark,
                 overview, leased_land, driveway_burden, contributions_for_roads, other_restrictions, notice,
                 info_open_date, info_update_date, next_date, expiry_date, management_fee, building_number, structure):
        self.post_type = post_type
        self.post_id = post_id
        self.user_id = user_id
        self.property_type = property_type
        self.property_name = property_name
        self.presentation_condition = presentation_condition
        self.price = price
        self.maximum_price = maximum_price
        self.move_in_date = move_in_date
        self.image = image
        self.address = address
        self.map = map
        self.access = access
        self.parking = parking
        self.floor_plan = floor_plan
        self.transaction_form = transaction_form
        self.exclusive_area = exclusive_area
        self.building_area = building_area
        self.land_area = land_area
        self.balcony_area = balcony_area
        self.site_area = site_area
        self.total_sales = total_sales
        self.price_range = price_range
        self.direction_access = direction_access
        self.road_conditions = road_conditions
        self.land_rights = land_rights
        self.building_coverage = building_coverage
        self.floor_area = floor_area
        self.use_area = use_area
        self.landmark = landmark
        self.overview = overview
        self.leased_land = leased_land
        self.driveway_burden = driveway_burden
        self.contributions_for_roads = contributions_for_roads
        self.other_restrictions = other_restrictions
        self.notice = notice
        self.info_open_date = info_open_date
        self.info_update_date = info_update_date
        self.next_date = next_date
        self.expiry_date = expiry_date
        self.management_fee = management_fee
        self.building_number = building_number
        self.structure = structure


def make_request(base_data: post_val):
    

    url = 'https://ymgfg.co.jp/wp-admin/post-new.php?post_type=' + base_data.post_type # Replace with the actual API endpoint

    # Params
    params = {
        'post': base_data.post_id,
        'action': 'edit',
        'meta-box-loader': 1,
        'meta-box-loader-nonce': '64385b526a',
        '_locale': 'user',
    }
    # Form data
    form_data = {
        '_wpnonce': '75cae2e6f6',
        '_wp_http_referer': '/wp-admin/post-new.php?post_type=' + base_data.post_type,
        'user_ID': base_data.user_id,
        'action': 'editpost',
        'originalaction': 'editpost',
        'post_type': base_data.post_type,
        'original_post_status': 'auto-draft',
        'referredby': 'https://ymgfg.co.jp/wp-admin/edit.php?post_type=baibai',
        '_wp_original_http_referer': 'https://ymgfg.co.jp/wp-admin/edit.php?post_type=' + base_data.post_type,
        'auto_draft': 1,
        'post_ID': base_data.post_id,
        'meta-box-order-nonce': 'c72bc59732',
        'closedpostboxesnonce': 'da6a4dc019',
        'samplepermalinknonce': 'a4e2506b5b',
        '_acf_screen': 'post',
        '_acf_post_id': base_data.post_id,
        '_acf_validation': 1,
        '_acf_nonce': 'ccf7655c5a',
        '_acf_changed': 0,
        'swl_nonce_meta_side': '4d0bf231b4',
        '_wp_http_referer': '/wp-admin/post-new.php?post_type=' + base_data.post_type,
        'swell_meta_related_posts': '',
        'swell_meta_youtube': '',
        'swell_meta_thumb_caption': '',
        'swell_meta_ttlbg': '',
        'swell_meta_ttl_pos': '',
        'swell_meta_show_pickbnr': '',
        'swell_meta_show_sidebar': '',
        'swell_meta_show_thumb': '',
        'swell_meta_show_index': '',
        'swell_meta_toc_target': '',
        'swell_meta_show_related': '',
        'swell_meta_show_author': '',
        'swell_meta_show_comments': '',
        'swell_meta_show_widget_top': 0,
        'swell_meta_show_widget_bottom': 0,
        'swell_meta_hide_before_index': 0,
        'swell_meta_hide_autoad': 0,
        'swell_meta_hide_sharebtn': 0,
        'swell_meta_hide_widget_cta': 0,
        'swl_nonce_meta_code': 'c845dd1092',
        '_wp_http_referer': '/wp-admin/post-new.php?post_type=' + base_data.post_type,
        'swell_meta_css': '',
        'swell_meta_css_plane': 0,
        'swell_meta_js': '',
        'swell_meta_js_plane': 0,
        'acf[field_63c7be4a24be6]': base_data.property_type,
        'acf[field_63c56d2a6ec4d]': base_data.property_name, #
        'acf[field_63f76b8cdd99c]': base_data.presentation_condition,
        'acf[field_63c56d2a6ee3a]': base_data.price,
        'acf[field_63c56d2a6ed96]': base_data.maximum_price,
        'acf[field_641ae05dbb6bd]': base_data.move_in_date,
        'acf[field_63c56d2a6ec84]': base_data.image[0]['source'],
        'acf[field_641ae1bcef3a4]': base_data.image[0]['description'],
        'acf[field_63c56d2a6ecba]': base_data.image[1]['source'],
        'acf[field_641ae2293119d]': base_data.image[1]['description'],
        'acf[field_641ae25d3119e]': base_data.image[2]['source'],
        'acf[field_641ae27b3119f]': base_data.image[2]['description'],
        'acf[field_641ae2e17e126]': base_data.image[3]['source'],
        'acf[field_641ae2f57e127]': base_data.image[3]['description'],
        'acf[field_641ae3077e128]': base_data.image[4]['source'],
        'acf[field_641ae3237e129]': base_data.image[4]['description'],
        'acf[field_641ae3337e12b]': base_data.image[5]['source'],
        'acf[field_641ae3317e12a]': base_data.image[5]['description'],
        'acf[field_641ae3697e12c]': base_data.image[6]['source'],
        'acf[field_641ae40b7e12d]': base_data.image[6]['description'],
        'acf[field_641ae4377e12e]': base_data.image[7]['source'],
        'acf[field_641ae44b7e12f]': base_data.image[7]['description'],
        'acf[field_641ae46d7e130]': base_data.image[8]['source'],
        'acf[field_641ae4737e131]': base_data.image[8]['description'],
        'acf[field_641ae4887e132]': base_data.image[9]['source'],
        'acf[field_641ae49a7e133]': base_data.image[9]['description'],
        'acf[field_63c56d2a6ecf2]': base_data.address,
        'acf[field_645505ecb1dc9]': base_data.map,
        'acf[field_63c56d2a6f30c]': base_data.access,
        'acf[field_63c56d2a6edcc]': base_data.parking,
        'acf[field_63c56d2a6f134]': base_data.floor_plan,
        'acf[field_63c56d2a6f0fd]': base_data.transaction_form,
        'acf[field_6419eec095412]': base_data.exclusive_area,
        'acf[field_63c56d2a6f024]': base_data.building_area,
        'acf[field_63c56d2a6efee]': base_data.land_area,
        'acf[field_63c56d2a6f29f]': base_data.balcony_area,
        'acf[field_63c56d2a6ed29]': base_data.site_area,
        'acf[field_63c56d2a6ed5f]': base_data.total_sales,
        'acf[field_63c56d2a6ee03]': base_data.price_range,
        'acf[field_63f7761fa4fdd]': base_data.direction_access,
        'acf[field_63c6bcafe89f8]': base_data.road_conditions,
        'acf[field_63c6be5de89fc]': base_data.land_rights,
        'acf[field_63c6bdbee89fa]': base_data.building_coverage,
        'acf[field_63c6bdf2e89fb]': base_data.floor_area,
        'acf[field_63c6bf42e89ff]': base_data.use_area,
        'acf[field_63c6bf65e8a00]': base_data.landmark,
        'acf[field_63c6c033e8a02]': base_data.overview,
        'acf[field_640da57bb2021]': base_data.leased_land,
        'acf[field_63c6c3969e570]': base_data.driveway_burden,
        'acf[field_640da72348b69]': base_data.contributions_for_roads,
        'acf[field_63c6bcefe89f9]': base_data.other_restrictions,
        'acf[field_63c56d2a6f3e5]': base_data.notice,
        'acf[field_63c56d2a6ef4b]': base_data.info_open_date,
        'acf[field_63c56d2a6ef14]': base_data.info_update_date,
        'acf[field_63c56d2a6ef81]': base_data.next_date,
        'acf[field_63c56d2a6eede]': base_data.expiry_date,
        'acf[field_640dacb2bfa4f]': base_data.management_fee,
        'acf[field_63c56d2a6eea8]': base_data.building_number,
        'acf[field_63c56d2a6f1a0]': base_data.structure,
        'acf[field_63c6c00de8a01]': '',
        'acf[field_640db0f18bfa8]': '',
        'acf[field_65d2dfc890417]': '',
        'um_content_restriction[_um_custom_access_settings]': 0,
        'um_content_restriction[_um_accessible]': 0,
        'um_content_restriction[_um_access_hide_from_queries]': 0,
        'um_content_restriction[_um_noaccess_action]': 0,
        'um_content_restriction[_um_restrict_by_custom_message]': 0,
        'um_content_restriction[_um_restrict_custom_message]': '',
        'um_content_restriction[_um_access_redirect]': 0,
        'um_content_restriction[_um_access_redirect_url]': '',
        'um_admin_save_metabox_restrict_content_nonce': 'baaf836119',
        '_wp_http_referer': '/wp-admin/post-new.php?post_type=' + base_data.post_type,
        'ssp_meta_robots': '',
        'ssp_meta_title': '',
        'ssp_meta_description': '',
        'ssp_meta_image': '',
        'ssp_meta_canonical': '',
        'ssp_meta_keyword': '',
        'ssp_nonce_name': '886168c63f',
        '_wp_http_referer': '/wp-admin/post-new.php?post_type=' + base_data.post_type,
        'post_author': 2,
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # response = requests.post(url, data=form_data, headers=headers)
    return url, params, form_data, headers
