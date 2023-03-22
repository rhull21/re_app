# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Tables: 
class DischargeGsa(models.Model):
    qid = models.AutoField(primary_key=True)
    id = models.ForeignKey('Observation', models.DO_NOTHING, db_column='id')
    discharge_cfs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge_gsa'


class Dryness(models.Model):
    dryid = models.IntegerField(primary_key=True)
    id = models.ForeignKey('Observation', models.DO_NOTHING, db_column='id')
    extent = models.CharField(max_length=10, blank=True, null=True)
    down_dryid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dryness'


class Feature(models.Model):
    fid = models.AutoField(primary_key=True)
    feature = models.TextField(blank=True, null=True)
    rm = models.ForeignKey('Rivermile', models.DO_NOTHING, db_column='rm', blank=True, null=True)
    featype = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feature'

class Observation(models.Model):
    fulcrum_id = models.CharField(max_length=38, blank=True, null=True)
    rm = models.ForeignKey('Rivermile', models.DO_NOTHING, db_column='rm', blank=True, null=True)
    obstype = models.CharField(max_length=38, blank=True, null=True)
    datet = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observation'


class Photos(models.Model):
    pid = models.AutoField(primary_key=True)
    id = models.ForeignKey(Observation, models.DO_NOTHING, db_column='id')
    photos_gen_url = models.CharField(max_length=2083, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photos'


class Reach(models.Model):
    reaid = models.AutoField(primary_key=True)
    reach = models.CharField(max_length=10, blank=True, null=True)
    upstream_rm = models.ForeignKey('Rivermile', models.DO_NOTHING, db_column='upstream_rm', blank=True, null=True)
    downstream_rm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reach'


class Remnant(models.Model):
    remid = models.AutoField(primary_key=True)
    id = models.ForeignKey(Observation, models.DO_NOTHING, db_column='id')
    approximate_area_sq_feet = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'remnant'


class Rivermile(models.Model):
    rm = models.DecimalField(primary_key=True, max_digits=5, decimal_places=2)
    position = models.TextField()  # This field type is a guess.
    latlong = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'rivermile'

# Views (note - these must have primary keys set manually in models.py!)
class DryLength(models.Model):
    rm_up = models.DecimalField(primary_key=True, max_digits=5, decimal_places=2, blank=True, null=False)
    rm_down = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dry_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dat = models.DateField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'dry_length'

class FeatureRm(models.Model):
    rm_rounded = models.DecimalField(primary_key=True, db_column='rm-rounded', max_digits=22, decimal_places=1, blank=True, null=False)  # Field renamed to remove unsuitable characters.
    feature = models.TextField(db_collation='utf8mb4_0900_ai_ci', blank=True, null=False)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'feature_rm'

class IsletaLen(models.Model):
    dat = models.DateField(primary_key=True, blank=True, null=False)
    sum_len = models.DecimalField(max_digits=28, decimal_places=2, blank=True, null=True)
    frac_len = models.DecimalField(max_digits=31, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'isleta_len'

class AcaciaLen(models.Model):
    dat = models.DateField(primary_key=True, blank=True, null=False)
    sum_len = models.DecimalField(max_digits=28, decimal_places=2, blank=True, null=True)
    frac_len = models.DecimalField(max_digits=31, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'acacia_len'

class AllLen(models.Model):
    thedate = models.DateField(primary_key=True, blank=True, null=False)
    isleta_sum_len = models.DecimalField(max_digits=28, decimal_places=2, blank=True, null=True)
    isleta_frac_len = models.DecimalField(max_digits=31, decimal_places=2, blank=True, null=True)
    acacia_sum_len = models.DecimalField(max_digits=28, decimal_places=2, blank=True, null=True)
    acacia_frac_len = models.DecimalField(max_digits=31, decimal_places=2, blank=True, null=True)
    combined_sum_len = models.DecimalField(max_digits=29, decimal_places=2, blank=True, null=True)
    combined_frac_len = models.DecimalField(max_digits=32, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'all_len'

class DryLengthAgg(models.Model):
    rm_up = models.DecimalField(primary_key=True, max_digits=5, decimal_places=2, blank=True)
    rm_down = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dry_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dat = models.DateField(blank=True, null=True)
    rm_down_rd = models.DecimalField(max_digits=22, decimal_places=1, blank=True, null=True)
    rm_up_rd = models.DecimalField(max_digits=22, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'dry_length_agg'