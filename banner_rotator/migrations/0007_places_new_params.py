# encoding: utf-8
from __future__ import unicode_literals
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Place'
        db.create_table('banner_rotator_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('width', self.gf('django.db.models.fields.SmallIntegerField')(default=None, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.SmallIntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('banner_rotator', ['Place'])

        # Adding unique constraint on 'Place', fields ['slug']
        db.create_unique('banner_rotator_place', ['slug'])

        # Adding field 'Banner.place'
        db.add_column('banner_rotator_banner', 'place', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='banners', to=orm['banner_rotator.Place']), keep_default=False)

        # Adding field 'Banner.alt'
        db.add_column('banner_rotator_banner', 'alt', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Banner.url_target'
        db.add_column('banner_rotator_banner', 'url_target', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True), keep_default=False)

        # Adding field 'Banner.max_views'
        db.add_column('banner_rotator_banner', 'max_views', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Banner.max_clicks'
        db.add_column('banner_rotator_banner', 'max_clicks', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Banner.start_at'
        db.add_column('banner_rotator_banner', 'start_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True), keep_default=False)

        # Adding field 'Banner.finish_at'
        db.add_column('banner_rotator_banner', 'finish_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True), keep_default=False)

        # Changing field 'Banner.campaign'
        db.alter_column('banner_rotator_banner', 'campaign_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['banner_rotator.Campaign']))

        # Deleting field 'Campaign.slug'
        db.delete_column('banner_rotator_campaign', 'slug')


    def backwards(self, orm):
        
        # Removing unique constraint on 'Place', fields ['slug']
        db.delete_unique('banner_rotator_place', ['slug'])

        # Deleting model 'Place'
        db.delete_table('banner_rotator_place')

        # Deleting field 'Banner.place'
        db.delete_column('banner_rotator_banner', 'place_id')

        # Deleting field 'Banner.alt'
        db.delete_column('banner_rotator_banner', 'alt')

        # Deleting field 'Banner.url_target'
        db.delete_column('banner_rotator_banner', 'url_target')

        # Deleting field 'Banner.max_views'
        db.delete_column('banner_rotator_banner', 'max_views')

        # Deleting field 'Banner.max_clicks'
        db.delete_column('banner_rotator_banner', 'max_clicks')

        # Deleting field 'Banner.start_at'
        db.delete_column('banner_rotator_banner', 'start_at')

        # Deleting field 'Banner.finish_at'
        db.delete_column('banner_rotator_banner', 'finish_at')

        # Changing field 'Banner.campaign'
        db.alter_column('banner_rotator_banner', 'campaign_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['banner_rotator.Campaign']))

        # Adding field 'Campaign.slug'
        db.add_column('banner_rotator_campaign', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(default='', populate_from='name', allow_duplicates=False, max_length=50, separator='-', blank=True, overwrite=False, db_index=True), keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'banner_rotator.banner': {
            'Meta': {'object_name': 'Banner'},
            'alt': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'banners'", 'null': 'True', 'blank': 'True', 'to': "orm['banner_rotator.Campaign']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'finish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_clicks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'banners'", 'to': "orm['banner_rotator.Place']"}),
            'start_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url_target': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'weight': ('django.db.models.fields.IntegerField', [], {})
        },
        'banner_rotator.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'banner_rotator.click': {
            'Meta': {'object_name': 'Click'},
            'banner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clicks'", 'to': "orm['banner_rotator.Banner']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'banner_clicks'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'banner_rotator.place': {
            'Meta': {'unique_together': "(('slug',),)", 'object_name': 'Place'},
            'height': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['banner_rotator']
